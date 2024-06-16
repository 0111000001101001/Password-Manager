import getpass, sqlite3, string, random, pyperclip, accounts
from tabulate import tabulate

# To-do list:
# - Add database encryption or store hashed versions of passwords.
# - Implement more error-handling.

def main():
    print("""
 ▄▄▄  ▄▄▄   ▄▄    ▄▄  ▐▄▄  ▄  ▄▌ ▄▄▄▄  ▄▄▄   ▄▄▄▄        ▌  ▄▄   ▄▄▄   ▐  ▄ ▄▄▄   ▄▄▄  ▄▄▄▄ ▄▄▄
▐█ ▄█▐█ ▀█ ▐█ ▀  ▐█ ▀  ██  █▌▐█ ██   █ ▀▄ █ ██  ██      ██ ▐███ ▐█ ▀█  █▌▐█▐█ ▀█ ▐█ ▀▀ ▀▄ ▀ ▀▄ █
 ██▀ ▄█▀▀█  ▀▀▀█▄ ▀▀▀█▄██ ▐█▐▐▌▐█▌   █▌▐▀▀▄ ▐█  ▐█▌    ▐█ ▌▐▌▐█ ▄█▀▀█ ▐█▐▐▌▄█▀▀█ ▄█ ▀█▄▐▀▀ ▄▐▀▀▄
▐█   ▐█  ▐▌▐█▄ ▐█▐█▄ ▐█▐█▌██▐█▌ ██  ██ ▐  █▌██  ██     ██ ██▌▐█▌▐█  ▐▌██▐█▌▐█  ▐▌▐█▄ ▐█▐█▄▄▌▐█ █▌
 ▀    ▀  ▀  ▀▀▀▀  ▀▀▀▀  ▀▀▀▀ ▀   ▀▀▀▀  ▀  ▀ ▀▀▀▀      ▀▀  ▀▀ ▀▀  ▀  ▀ ▀  ▀  ▀  ▀  ▀▀▀▀   ▀▀▀ ▀  ▀
""")
    
    account_menu_input = input("""Account Menu:
Create a new account (1)
Log-in to an existing account (2)
Quit program (q)

: """).lower()
    
    master_accounts_db_table()
    
    while True:
        if account_menu_input == '1':
            if create_account():
                # If account creation succeeds, establish a distinct table for storing the current user's passwords.
                print("\n     ʕ⊃•ᴥ•ʔ⊃ Welcome! ⊂ʕ•ᴥ•⊂ʔ")
                password_manager_db_table()
                menu_options()
                break
            else:
                # Else, quit program.
                account_conn.close()
                print("\nExiting program... ʕ •ᴥ•ʔ\n")
                quit()
        elif account_menu_input == '2':
            if authenticate_master_pass():
                # If log-in succeeds, connect to the current user's password manager.
                print("\n     ʕ⊃•ᴥ•ʔ⊃ Welcome! ⊂ʕ•ᴥ•⊂ʔ")
                password_manager_db_table()
                menu_options()
                break
            else:
                # Else, quit program.
                account_conn.close()
                print("Too many failed attempts, exiting program... ʕ •ᴥ•ʔ\n")
                quit()
        elif account_menu_input == 'q':
            print("")
            account_conn.close()
            quit()
        else:
            account_menu_input = input("Invalid input, try again.\n: ").lower()

def master_accounts_db_table():
    # Decalres commonly used variables and establishes a table comprised of two columns, in which account credentials are stored.
    global account_conn, account_cursor
    account_conn = sqlite3.connect("password_manager.db")
    account_cursor = account_conn.cursor()

    account_conn.execute("""CREATE TABLE IF NOT EXISTS account_credentials
        (master_user TEXT NOT NULL,
        master_pass TEXT NOT NULL)""")

def password_manager_db_table():
    # Decalres commonly used variables and establishes a table comprised of three columns, 
    # each created table corresponds to the current user. Used for storing personal passwords.
    global conn, cursor
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()

    conn.execute(f"""CREATE TABLE IF NOT EXISTS passwords_{current_user}
        (website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL)""")

def create_account():
    print("_" * 35 + "\n\nCreate Account:")
    
    while True:
        # Checks to see if the inputted username is comprised of only letters and numbers, 
        # and has a minimum length of 3 characters and a maximum of 16.
        master_user = input("\nUsername: ")

        if not accounts.validate_username(master_user):
            print("Usernames can only contain letters and numbers with a minimum length of 3 characters and a maximum length of 16. Try again.")
            continue
    
        # Checks to see whether or not the inputted username already exists in the account credentials table.
        sql = "SELECT * FROM account_credentials WHERE master_user = ?"
        account_cursor.execute(sql, (master_user,))

        if account_cursor.fetchone():
            print("This username seems to be taken. Try entering a different one.")
            continue
        else:
            print("Username is available.\n")
            break
    
    while True:
        # Checks that the password is at least 8 characters long and less than 128 characters long.
        master_pass = input("Master password: ")
        if accounts.validate_password(master_pass):
            break
        else:
            print("Master password needs to be at least 8 characters long with a limit of 128 characters. Try again.\n")
            continue

    confirm = input("Sign up for this account? (y/n): ").lower()

    while True:
        # Inserts the newly created account into the table. And declares the current user of the program.
        if confirm == 'y':
            user_input = (master_user, master_pass)
            sql = "INSERT INTO account_credentials(master_user, master_pass) VALUES(?, ?)"
            account_cursor.execute(sql, user_input)
            account_conn.commit()

            print("\nAccount successfully created. ＼ʕ •ᴥ•ʔ／\n\n" + "_" * 35)
            global current_user
            current_user = master_user
            return True
        elif confirm == 'n':
            return False
        else:
            confirm = input("Invalid input, try again.\n: ").lower()

def authenticate_master_pass(): 
    # Limited attempts to gain access to the program. Provides an authentication check.
    for i in range(5):
        exist_user = input("_" * 35 + "\n\nLog-in:\n\nUsername: ").strip()
        exist_pass = getpass.getpass("Master password: ").strip()
        user_input = (exist_user, exist_pass)

        sql = "SELECT * FROM account_credentials WHERE master_user = ? AND master_pass = ?"
        account_cursor.execute(sql, user_input)

        if account_cursor.fetchone():
            # If authentication succeeds, it returns True, and declares the current user of the program.
            global current_user
            current_user = exist_user
            print("_" * 35)
            return True
        else:
            print("\nIncorrect credentials.")
    else:
        # Else, returns False when authentication fails.
        return False

def menu_options():
    # The main menu of the program that displays all the commands to choose from.
    print("_" * 35)
    choice = input("""\nSelect from the following commands:
                   
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
            add_password()
            break
        elif choice == '2':
            edit_password()
            break
        elif choice == '3':
            delete_pass()
            break
        elif choice == '4':
            generate_password()
            break
        elif choice == '5':
            search_password()
            break
        elif choice == '6':
            list_passwords()
            break
        elif choice == '7':
            change_account_password()
            break
        elif choice == 'q':
            account_conn.close()
            conn.close()
            print("\nConnection closed. Exiting program... ʕ •ᴥ•ʔ\n")
            quit()
        else:
            choice = input("\nUndefined command, try again.\n: ").lower()

def add_password():
    # Receives website and username inputs and checks if they already exist in the passwords_{current_user} table.
    new_web = input("_" * 35 + "\n\nWebsite or application: ").strip()
    new_user = input("Username or email: ").strip()
    user_input = (new_web, new_user)

    sql = f"SELECT * FROM passwords_{current_user} WHERE website = ? AND username = ?"
    cursor.execute(sql, user_input)

    if cursor.fetchone():
        # If entry already exists, notify the user.
        print("\nAn entry already exists with those exact inputs. ʕ ´•̥̥̥ ᴥ•̥̥̥`ʔ")
    else:
        # Else, inserts the entry into the table.
        new_pass = input("Password: ").strip()
        user_input = (new_web, new_user, new_pass)

        sql = f"INSERT INTO passwords_{current_user}(website, username, password) VALUES(?, ?, ?)"
        cursor.execute(sql, user_input)
        conn.commit()

        print("\nPassword successfully added. ＼ʕ •ᴥ•ʔ／")

    menu_options()

def edit_password(): 
    # Takes the username and website corresponding to a password and checks to see 
    # if they exist in the passwords_{current_user} table. 
    web_of_pass = input("_" * 35 + "\n\nEnter the website or app of the password that you would like to edit: ").strip()
    user_of_pass = input("Enter the username or email of the password that you would like to edit: ").strip()
    user_input = (web_of_pass, user_of_pass)

    sql = f"SELECT * FROM passwords_{current_user} WHERE website = ? AND username = ?"
    cursor.execute(sql, user_input)

    if cursor.fetchone():
        # If entry is present, the user is asked to input the updated password, which is then updated. 
        change_pass = input("Enter the updated password: ").strip()
        confirm = input("\nAre you sure you want to edit this entry? (y/n): ").lower()

        while True:
            if confirm == 'y':
                user_input = (change_pass, web_of_pass, user_of_pass)
                sql = f"UPDATE passwords_{current_user} SET password = ? WHERE website = ? AND username = ?"
                cursor.execute(sql, user_input)

                conn.commit()
                print("\nPassword successfully changed. ＼ʕ •ᴥ•ʔ／")
                break
            elif confirm == 'n':
                print("\nReturning back to menu...")
                break
            else:
                confirm = input("Invalid input, try again.\n:  ").lower()
    else:
        # Else, if the entry is not present, returns to menu.
        print("\nEntry not found. No password updated. ʕ ´•̥̥̥ ᴥ•̥̥̥`ʔ")

    menu_options()

def delete_pass():
    # Takes the username and website corresponding to a password and checks to see if they exist. 
    del_web = input("_" * 35 + "\n\nEnter the website/app of the password that you would like to delete: ").strip()
    del_user = input("Enter the username/email of the password that you would like to delete: ").strip()
    user_input = (del_web, del_user)

    sql = f"SELECT * FROM passwords_{current_user} WHERE website = ? AND username = ?"
    cursor.execute(sql, user_input)

    if cursor.fetchone():
        # If entry is present, the user is asked whether or not they want to delete it.
        confirm = input("\nAre you sure you want to delete this entry? (y/n): ").lower()
        while True:
            if confirm == 'y':
                sql = f"DELETE FROM passwords_{current_user} WHERE website = ? AND username = ?"
                cursor.execute(sql, user_input)
                conn.commit()

                print("\nPassword successfully deleted. ＼ʕ •ᴥ•ʔ／")
                break
            elif confirm == 'n':
                print("\nReturning back to menu...")
                break
            else:
                confirm = input("Invalid input, try again.\n:  ").lower()
    else:
        # Else, if the entry is not present, returns to menu.
        print("\nEntry not found. No password deleted. ʕ ´•̥̥̥ ᴥ•̥̥̥`ʔ")

    menu_options()

def generate_password():
    # Generates a random 32-character password and copies it to clipboard.
    char_set = string.ascii_letters + string.digits + "@&$%?!#*^+-."
    password = ""

    for i in range(32):
        random_char = random.choice(char_set)
        password += random_char

    print("_" * 35 + "\n\nGenerated password:", password)
    copy = input("Copy generated password to clipboard? (y/n): ").lower()

    while True:
        if copy == 'y':
            pyperclip.copy(password)
            print("\nPassword successfully copied to clipboard. ＼ʕ •ᴥ•ʔ／")
            break
        elif copy == 'n':
            print("\nReturning to menu...")
            break
        else:
            copy = input("Invalid input, try again.\n: ").lower()

    menu_options()

def search_password():
    # Helps the user search for an existing password by printing all entries 
    # in which the website name starts with the user's input
    search = input("_" * 35 + "\n\nWebsite name: ").lower()
    search = search + "%"

    sql = f"SELECT * FROM passwords_{current_user} WHERE website LIKE ?"
    cursor.execute(sql, (search,))
    rows = cursor.fetchall()

    if rows:
        print("_" * 35 + "\n")
        headers = ["Website", "Username", "Password"]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print("This entry does not exist. ʕ ´•̥̥̥ ᴥ•̥̥̥`ʔ")

    print("_" * 35 + "\n")
    choice = input("""Select from the following:

Go back to menu (1)
Quit program (q)
: """).lower()
    
    while True:
            if choice == '1':
                print("\nReturning back to menu...")
                menu_options()
                break
            elif choice == 'q':
                account_conn.close()
                conn.close()
                print("\nConnection closed. Exiting program... ʕ •ᴥ•ʔ\n")
                quit()
            else:
                choice = input("Invalid input, try again.\n:  ").lower()
    
def list_passwords():
    # Selects all rows, rearranges in alphabetical order, and prints the table that stores the user's passwords.
    print("_" * 35 + "\n")

    sql = f"SELECT * FROM passwords_{current_user} ORDER BY website ASC"
    cursor.execute(sql)
    rows = cursor.fetchall()

    headers = ["Website", "Username", "Password"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))

    print("_" * 35 + "\n")
    choice = input("""Select from the following:

Go back to menu (1)
Quit program (q)
: """).lower()
    
    while True:
            if choice == '1':
                print("\nReturning back to menu...")
                menu_options()
                break
            elif choice == 'q':
                account_conn.close()
                conn.close()
                print("\nConnection closed. Exiting program... ʕ •ᴥ•ʔ\n")
                quit()
            else:
                choice = input("Invalid input, try again.\n:  ").lower()

def change_account_password():
    current_pass = input("_" * 35 + "\n\nEnter current password: ")

    while True:
        # Checks to see if the user entered their correct master password.
        user_input = (current_user, current_pass)

        sql = "SELECT * FROM account_credentials WHERE master_user = ? AND master_pass = ?"
        account_cursor.execute(sql, user_input)

        if account_cursor.fetchone():
            # If user's input is correct, ask for an updated password.
            updated_pass = input("New password: ")
            confirm = input('\nType "CONFIRM" to update password or "QUIT" to exit: ' )

            while True:
                if confirm == 'CONFIRM':
                    # If CONFIRM, updates the account_credentials table with the newly entered password and break out of the loop.
                    user_input = (updated_pass, current_user)
                    sql = "UPDATE account_credentials SET master_pass = ? WHERE master_user = ?"
                    account_cursor.execute(sql, user_input)
                    account_conn.commit()

                    print("\nMaster password successfully updated. ＼ʕ •ᴥ•ʔ／")
                    break
                elif confirm == 'QUIT':
                    # If QUIT, quits program.
                    account_conn.close()
                    conn.close()
                    print("\nConnection closed. Exiting program... ʕ •ᴥ•ʔ\n")
                    quit()
                else:
                    # Reprompts the user if invalid input.
                    confirm = input("Invalid input, try again.\n:  ")
            break

        else:
            # Else, reprompt the user for the correct master password.
            current_pass = input("\nIncorrect password, try again.\n: ")

    menu_options()

main()