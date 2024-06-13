import getpass, sqlite3, string, random, pyperclip
from tabulate import tabulate

# To-do list:
# - Add database encryption or store hashed version of passwords.
# - Implement more error-handling.

def main():
    print("""
 ▄▄▄  ▄▄▄   ▄▄    ▄▄  ▐▄▄  ▄  ▄▌ ▄▄▄▄  ▄▄▄   ▄▄▄▄        ▌  ▄▄   ▄▄▄   ▐  ▄ ▄▄▄   ▄▄▄  ▄▄▄▄ ▄▄▄
▐█ ▄█▐█ ▀█ ▐█ ▀  ▐█ ▀  ██  █▌▐█ ██   █ ▀▄ █ ██  ██      ██ ▐███ ▐█ ▀█  █▌▐█▐█ ▀█ ▐█ ▀▀ ▀▄ ▀ ▀▄ █
 ██▀ ▄█▀▀█  ▀▀▀█▄ ▀▀▀█▄██ ▐█▐▐▌▐█▌   █▌▐▀▀▄ ▐█  ▐█▌    ▐█ ▌▐▌▐█ ▄█▀▀█ ▐█▐▐▌▄█▀▀█ ▄█ ▀█▄▐▀▀ ▄▐▀▀▄
▐█   ▐█  ▐▌▐█▄ ▐█▐█▄ ▐█▐█▌██▐█▌ ██  ██ ▐  █▌██  ██     ██ ██▌▐█▌▐█  ▐▌██▐█▌▐█  ▐▌▐█▄ ▐█▐█▄▄▌▐█ █▌
 ▀    ▀  ▀  ▀▀▀▀  ▀▀▀▀  ▀▀▀▀ ▀   ▀▀▀▀  ▀  ▀ ▀▀▀▀      ▀▀  ▀▀ ▀▀  ▀  ▀ ▀  ▀  ▀  ▀  ▀▀▀▀   ▀▀▀ ▀  ▀
""")
    
    acc_menu_input = input("""Account Menu:
Create new account (1)
Log-into an existing acount (2)
Quit program (q)

: """).lower()
    
    pm_accounts()
    
    while True:
        if acc_menu_input == '1':
            if create_acc():
                # If account creation succeeds, establish a distinct table for storing the current user's passwords.
                print("\n     ʕ⊃•ᴥ•ʔ⊃ Welcome! ⊂ʕ•ᴥ•⊂ʔ")
                pm_passwords()
                options()
                break
            else:
                # Else, quit program.
                account_conn.close()
                print("\nExiting program... ʕ •ᴥ•ʔ\n")
                quit()
        elif acc_menu_input == '2':
            if authenticate():
                # If log-in succeeds, connect to the current user's password manager.
                print("\n     ʕ⊃•ᴥ•ʔ⊃ Welcome! ⊂ʕ•ᴥ•⊂ʔ")
                pm_passwords()
                options()
                break
            else:
                # Else, quit program.
                account_conn.close()
                print("Too many failed attempts, exiting program... ʕ •ᴥ•ʔ\n")
                quit()
        elif acc_menu_input == 'q':
            print("")
            account_conn.close()
            quit()
        else:
            acc_menu_input = input("Invalid input, try again.\n: ").lower()

def pm_accounts():
    # Decalres commonly used variables and establishes the database comprised of a table with two columns. 
    # Establishes a table for storing master user credentials.
    global account_conn, account_cursor
    account_conn = sqlite3.connect("pm_accounts.db")
    account_cursor = account_conn.cursor()

    account_conn.execute('''CREATE TABLE IF NOT EXISTS pm_accounts
        (master_user TEXT NOT NULL,
        master_pass TEXT NOT NULL)''')

def pm_passwords():
    # Decalres commonly used variables and establishes the database comprised of a table with three columns. 
    # Establishes a table for each individual user.
    global conn, cursor, current_user_db
    current_user_db = f"pm_passwords_{current_user}.db"
    conn = sqlite3.connect(current_user_db)
    cursor = conn.cursor()

    conn.execute('''CREATE TABLE IF NOT EXISTS pm_passwords
        (website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL)''')

def create_acc():
    print("_" * 35 + "\n\nCreate Account:")
    
    while True:
        while True:
            # Checks to see if inputted username is comprised of only letters and numbers, 
            # and has a minimum length of 3 characters and maximum of 16.
            master_user = input("\nUsername: ")
            user_length = len(master_user)
            special_char = False

            for char in master_user:
                if not char.isalnum():
                    special_char = True

            if special_char == True or user_length < 3 or user_length > 16:
                print("Usernames can only contain letters, numbers, a minimum length of 3 characters and a maximum length of 16. Try again.")
            else:
                break
        
        # Checks to see whether or not the inputted username already exists in the database.
        sql_check = """SELECT * FROM pm_accounts WHERE master_user = ?"""
        account_cursor.execute(sql_check, (master_user,))
        account_row = account_cursor.fetchone()

        if account_row:
            print("This username seems to be taken. Try entering a different one.")
        else:
            print("Username is available.\n")
            break

    master_pass = input("Master password: ").strip()
    confirm = input("Sign up for this account? (y/n): ").lower()

    while True:
        # Inserts the newly created account into the database. And declares the current user of the program.
        if confirm == 'y':
            user_input = (master_user, master_pass)
            sql = """INSERT INTO pm_accounts(master_user, master_pass) VALUES(?, ?)"""
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

def authenticate(): 
    # Limited attempts to gain access to the program. Provides an authentication check.
    for i in range(5):
        exist_user = input("_" * 35 + "\n\nLog-in:\n\nUsername: ").strip()
        exist_pass = getpass.getpass("Master password: ").strip()
        user_input = (exist_user, exist_pass)

        sql_check = """SELECT * FROM pm_accounts WHERE master_user = ? AND master_pass = ?"""
        account_cursor.execute(sql_check, user_input)
        account_row = account_cursor.fetchone()

        if account_row:
            # If authentication succeeds, returns True, and declares the current user of the program.
            global current_user
            current_user = exist_user
            print("_" * 35)
            return True
        else:
            print("\nIncorrect credentials.")
    else:
        # Else, returns False when authentication fails.
        return False

def options():
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
            add_pass()
            break
        elif choice == '2':
            edit_pass()
            break
        elif choice == '3':
            delete_pass()
            break
        elif choice == '4':
            pass_gen()
            break
        elif choice == '5':
            pass_search()
            break
        elif choice == '6':
            pass_list()
            break
        elif choice == '7':
            change_acc_pass()
            break
        elif choice == 'q':
            account_conn.close()
            conn.close()
            print("\nConnection closed. Exiting program... ʕ •ᴥ•ʔ\n")
            quit()
        else:
            choice = input("\nUndefined command, try again.\n: ").lower()

def add_pass():
    # Receives three inputs and checks if they are already in database.
    new_web = input("_" * 35 + "\n\nName of website or application: ").strip()
    new_user = input("Username or email: ").strip()
    user_input = (new_web, new_user)

    sql_check = """SELECT * FROM pm_passwords WHERE website = ? AND username = ?"""
    cursor.execute(sql_check, user_input)
    row = cursor.fetchone()

    if row:
        # If entry already exists, notifies the user.
        print("\nAn entry already exists with those exact inputs. ʕ ´•̥̥̥ ᴥ•̥̥̥`ʔ")
    else:
        # Else, inserts the entry into the database.
        new_pass = input("Password: ").strip()
        user_input = (new_web, new_user, new_pass)
        sql = """INSERT INTO pm_passwords(website, username, password) VALUES(?, ?, ?)"""

        cursor.execute(sql, user_input)
        conn.commit()

        print("\nPassword successfully added. ＼ʕ •ᴥ•ʔ／")

    options()

def edit_pass(): 
    # Takes the username and website corresponding to a password and checks to see if they are present in the database. 
    web_of_pass = input("_" * 35 + "\n\nEnter the website/app of the password that you would like to edit: ").strip()
    user_of_pass = input("Enter the username/email of the password that you would like to edit: ").strip()
    user_input = (web_of_pass, user_of_pass)

    sql_check = """SELECT * FROM pm_passwords WHERE website = ? AND username = ?"""
    cursor.execute(sql_check, user_input)
    row = cursor.fetchone()

    if row:
        # If entry is present, the user is asked to input the updated password, which is then updated in the database. 
        change_pass = input("Enter the updated password: ").strip()
        confirm = input("\nAre you sure you want to edit this entry? (y/n): ").lower()

        while True:
            if confirm == 'y':
                user_input = (change_pass, web_of_pass, user_of_pass)
                sql_update = """UPDATE pm_passwords SET password = ? WHERE website = ? AND username = ?"""   
                cursor.execute(sql_update, user_input)

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

    options()

def delete_pass():
    # Takes the username and website corresponding to a password and checks to see if they are present in the database. 
    del_web = input("_" * 35 + "\n\nEnter the website/app of the password that you would like to delete: ").strip()
    del_user = input("Enter the username/email of the password that you would like to delete: ").strip()
    user_input = (del_web, del_user)

    sql_check = """SELECT * FROM pm_passwords WHERE website = ? AND username = ?"""
    cursor.execute(sql_check, user_input)
    row = cursor.fetchone()

    if row:
        # If entry is present, the user is asked whether or not that want to delete it.
        confirm = input("\nAre you sure you want to delete this entry? (y/n): ").lower()
        while True:
            if confirm == 'y':
                sql = """DELETE FROM pm_passwords WHERE website = ? AND username = ?"""
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

    options()

def pass_gen():
    # Generates a random 32 character password and copies it to clipboard.
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

    options()

def pass_search():
    # Helps the user search for an existing password by printing all entries 
    # in which the website name starts with the user's input
    search = input("_" * 35 + "\n\nEnter website name: ").lower()
    search = search + "%"

    sql = """SELECT * FROM pm_passwords WHERE website LIKE ?"""
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
                options()
                break
            elif choice == 'q':
                account_conn.close()
                conn.close()
                print("\nConnection closed. Exiting program... ʕ •ᴥ•ʔ\n")
                quit()
            else:
                choice = input("Invalid input, try again.\n:  ").lower()
    
def pass_list():
    # Selects all rows in alphabetical order and prints the database.
    print("_" * 35 + "\n")

    sql = """SELECT * FROM pm_passwords ORDER BY website ASC"""
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
                options()
                break
            elif choice == 'q':
                account_conn.close()
                conn.close()
                print("\nConnection closed. Exiting program... ʕ •ᴥ•ʔ\n")
                quit()
            else:
                choice = input("Invalid input, try again.\n:  ").lower()

def change_acc_pass():
    current_pass = input("_" * 35 + "\n\nEnter current password: ")

    while True:
        # Checks to see if user inputted their correct master password.
        user_input = (current_user, current_pass)

        sql_check = """SELECT * FROM pm_accounts WHERE master_user = ? AND master_pass = ?"""
        account_cursor.execute(sql_check, user_input)
        account_row = account_cursor.fetchone()

        if account_row:
            # If they inputted correct master password, ask for updated password.
            updated_pass = input("New password: ")
            confirm = input('\nType "CONFIRM" to update password or "QUIT" to exit: ' )

            while True:
                if confirm == 'CONFIRM':
                    # If CONFIRM, updates the pm_account database with the newly entered password and break out of the loop.
                    user_input = (updated_pass, current_user)
                    sql = """UPDATE pm_accounts SET master_pass = ? WHERE master_user = ?"""
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
                    # Reprompts user if invalid input.
                    confirm = input("Invalid input, try again.\n:  ")
            break

        else:
            # Else, reprompt user for the correct master password.
            current_pass = input("\nIncorrect password, try again.\n: ")

    options()

main()
