import pyperclip, string, random, database_utils
from tabulate import tabulate
from database_utils import close_all_db_connections_and_exit
from validation_utils import get_valid_master_password
from misc import confirm_user_input, return_to_menu
from crypto_utils import decrypt_all_entries

def menu_options(current_user):
    choice = input("_" * 35 +
"""\n\nSelect from the following commands:

- Add new password (1)
- Update an existing password (2)
- Delete an existing password (3)
- Generate a random password (4)
- Search for an existing password (5)
- View full list of entries (6)
- Change master password (7)
- Quit program (q)

: """).lower().strip()
    
    while True:
        if choice == '1':
            add_password(current_user)
            break
        elif choice == '2':
            update_password(current_user)
            break
        elif choice == '3':
            delete_password(current_user)
            break
        elif choice == '4':
            generate_password()
            break
        elif choice == '5':
            search_password(current_user)
            break
        elif choice == '6':
            list_passwords(current_user)
            break
        elif choice == '7':
            change_account_password(current_user)
            break
        elif choice == 'q':
            close_all_db_connections_and_exit()
        else:
            choice = input("Invalid input, try again.\n: ").lower().strip()

def add_password(current_user):
    new_web = input("\nWebsite or application: ").strip()
    new_user = input("Username or email: ").strip()
    new_pass = input("Password: ")

    database_utils.add_password_to_db(current_user, new_web, new_user, new_pass)
    print("\nPassword successfully added. ＼ʕ •ᴥ•ʔ／")

def update_password(current_user):
    while True:
        entry_id = input("\nEnter the entry ID to update: ").strip()
        if not entry_id.isnumeric():
            print("Invalid input, entry ID's are integers.")
        else:
            break

    result = database_utils.update_password_in_db(current_user, entry_id)
    if result == "updated":
        print("\nPassword successfully updated. ＼ʕ •ᴥ•ʔ／")
    elif result == "cancelled":
        print("\nReturning back to menu...")
    elif result == "not_found":
        print("\nEntry not found. No password updated. ʕ ´•̥̥̥ ᴥ•̥̥̥`ʔ")

def delete_password(current_user):
    while True:
        entry_id = input("\nEnter the entry ID to delete: ").strip()
        if not entry_id.isnumeric():
            print("Invalid input, entry ID's are integers.")
        else:
            break

    result = database_utils.delete_password_from_db(current_user, entry_id)
    if result == "deleted":
        print("\nPassword successfully deleted. ＼ʕ •ᴥ•ʔ／")
    elif result == "cancelled":
        print("\nReturning back to menu...")
    elif result == "not_found":
        print("\nEntry not found. No password deleted. ʕ ´•̥̥̥ ᴥ•̥̥̥`ʔ")

def generate_password():
    # Joins letters, numbers, and punctuations and produces a random 32-byte string, 
    # which can quickly be copied to clipboard.
    char_set = string.ascii_letters + string.digits + "@&$%?!#*^+-."
    password = ""

    for i in range(32):
        random_char = random.choice(char_set)
        password += random_char

    print("_" * 35 + "\n\nGenerated password:", password)
    confirm = input("Copy generated password to clipboard? (y/n): ").lower()

    if confirm_user_input(confirm):
        pyperclip.copy(password)
        print("\nPassword successfully copied to clipboard. ＼ʕ •ᴥ•ʔ／")
    else:
        print("\nReturning to menu...")

def search_password(current_user):
    # Searches for an entry using website name, if found, decrypts columns and prints result.
    search_web = input("\nWebsite name: ").lower() + "%"
    rows = database_utils.search_passwords_in_db(current_user, search_web)
    
    if rows:
        print("_" * 35 + "\n")
        decrypted_rows = decrypt_all_entries(current_user, rows)

        headers = ["ID", "Name", "Username", "Password"]
        print(tabulate(decrypted_rows, headers=headers, tablefmt="grid"))

        return_to_menu()
    else:
        print("\nNo matching entries found. ʕ ´•̥̥̥ ᴥ•̥̥̥`ʔ")

def list_passwords(current_user):
    # Selects all rows, decrypts the password column and prints result.
    rows = database_utils.get_all_passwords_from_db(current_user)
    decrypted_rows = decrypt_all_entries(current_user, rows)

    print("_" * 35 + "\n")

    headers = ["ID", "Name", "Username", "Password"]
    print(tabulate(decrypted_rows, headers=headers, tablefmt="grid"))

    return_to_menu()

def change_account_password(current_user):
    # Verifies current master password and prompts for an updated valid master password. Then, updates it in the database.
    current_pass = input("_" * 35 + "\n\nCurrent password: ")

    while True:
        # Checks to see if the user entered their correct master password.
        if database_utils.verify_master_account_credentials(current_user, current_pass):
            print("\nNow, enter the updated version.")
            updated_pass = get_valid_master_password()

            confirm = input('\nType "CONFIRM" to update password or "QUIT" to exit: ' )

            while True:
                if confirm == 'CONFIRM':
                    # If CONFIRM, updates the account_credentials table with the newly entered password and break out of the loop.
                    database_utils.update_master_password(current_user, updated_pass)
                    print("\nMaster password successfully updated. ＼ʕ •ᴥ•ʔ／")
                    break
                elif confirm == 'QUIT':
                    close_all_db_connections_and_exit()
                else:
                    confirm = input("Invalid input, try again.\n:  ")
            break

        else:
            # Else, reprompt the user for the correct master password.
            current_pass = input("\nIncorrect password, try again.\n: ")