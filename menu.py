import pyperclip, string, random, database_utils
from tabulate import tabulate
from validation_utils import get_valid_master_password

def menu_options(current_user):
    choice = input("_" * 35 +
"""\n\nSelect from the following commands:

- Add new password (1)
- Edit an existing password (2)
- Delete an existing password (3)
- Generate a random password (4)
- Search for an existing password (5)
- View full list of entries (6)
- Change master password (7)
- Quit program (q)

: """).lower()
    
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
            print("\nExiting program... ʕ •ᴥ•ʔ\n")
            quit()
        else:
            choice = input("Invalid input, try again.\n: ")

def add_password(current_user):
    new_web = input("\nWebsite or application: ").strip()
    new_user = input("Username or email: ").strip()

    if database_utils.add_password_to_db(current_user, new_web, new_user):
        print("\nAn entry already exists with those exact inputs. ʕ ´•̥̥̥ ᴥ•̥̥̥`ʔ")
    else:
        print("\nPassword successfully added. ＼ʕ •ᴥ•ʔ／")

def update_password(current_user):
    web_of_pass = input("\nWebsite or application of the password to edit: ").strip()
    user_of_pass = input("Username or email of the password to edit: ").strip()

    result = database_utils.update_password_in_db(current_user, web_of_pass, user_of_pass)
    if result == "updated":
        print("\nPassword successfully updated. ＼ʕ •ᴥ•ʔ／")
    elif result == "cancelled":
        print("\nReturning back to menu...")
    elif result == "not_found":
        print("\nEntry not found. No password updated. ʕ ´•̥̥̥ ᴥ•̥̥̥`ʔ")

def delete_password(current_user):
    del_web = input("\nWebsite or application of the password to delete: ").strip()
    del_user = input("Username or email of the password to delete: ").strip()

    result = database_utils.delete_password_from_db(current_user, del_web, del_user)
    if result == "deleted":
        print("\nPassword successfully deleted. ＼ʕ •ᴥ•ʔ／")
    elif result == "cancelled":
        print("\nReturning back to menu...")
    elif result == "not_found":
        print("\nEntry not found. No password deleted. ʕ ´•̥̥̥ ᴥ•̥̥̥`ʔ")

def generate_password():
    char_set = string.ascii_letters + string.digits + "@&$%?!#*^+-."
    password = ""

    for i in range(32):
        random_char = random.choice(char_set)
        password += random_char

    print("_" * 35 + "\n\nGenerated password:", password)
    confirm = input("Copy generated password to clipboard? (y/n): ").lower()

    while True:
        if confirm == 'y':
            pyperclip.copy(password)
            print("\nPassword successfully copied to clipboard. ＼ʕ •ᴥ•ʔ／")
            break
        elif confirm == 'n':
            print("\nReturning to menu...")
            break
        else:
            confirm = input("Invalid input, try again.\n: ").lower()

def search_password(current_user):
    search_pass = input("\nWebsite name: ").lower() + "%"
    rows = database_utils.search_passwords_in_db(current_user, search_pass)
    
    if rows:
        print("_" * 35 + "\n")
        headers = ["Website", "Username", "Password"]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print("No matching entries found. ʕ ´•̥̥̥ ᴥ•̥̥̥`ʔ")

def list_passwords(current_user):
    rows = database_utils.get_all_passwords_from_db(current_user)
    print("\n")
    headers = ["Website", "Username", "Password"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def change_account_password(current_user):
    current_pass = input("_" * 35 + "\n\nCurrent password: ")

    while True:
        # Checks to see if the user entered their correct master password.
        if database_utils.verify_master_account_credentials(current_user, current_pass):
            # If user's input is correct, ask for an updated password.
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
                    # If QUIT, quits program.
                    print("\nConnection closed. Exiting program... ʕ •ᴥ•ʔ\n")
                    quit()
                else:
                    # Reprompts the user if invalid input.
                    confirm = input("Invalid input, try again.\n:  ")
            break

        else:
            # Else, reprompt the user for the correct master password.
            current_pass = input("\nIncorrect password, try again.\n: ")