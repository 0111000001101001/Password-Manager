import getpass
import sqlite3
import string
import random
import pyperclip

# To-do list:
# - Add database encryption or store hashed version of passwords.
# - Dedicate a seperate database for each individual user.
# - Implement more error-handling.
# - Registering username can't have special characters.
# - Sort passwords in alphabetical order of the website/app name.
# - Ability to change user password.

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
                print("\n     ʕ⊃•ᴥ•ʔ⊃ Welcome! ⊂ʕ•ᴥ•⊂ʔ")
                pm_passwords()
                options()
                break
            else:
                print("\nQuiting program...")
                quit()
        elif acc_menu_input == '2':
            if authenticate():
                print("\n     ʕ⊃•ᴥ•ʔ⊃ Welcome! ⊂ʕ•ᴥ•⊂ʔ")
                pm_passwords()
                options()
                break
            else:
                print("Too many failed attempts, exiting program... ʕ>⌓<ʔ\n")
                quit()
        elif acc_menu_input == 'q':
            print("")
            quit()
        else:
            acc_menu_input = input("Invalid input, try again.\n: ")

def pm_accounts():
    global account_conn
    account_conn = sqlite3.connect("pm_accounts.db")
    global account_cursor
    account_cursor = account_conn.cursor()

    account_conn.execute('''CREATE TABLE IF NOT EXISTS pm_accounts
        (master_user TEXT NOT NULL,
        master_pass TEXT NOT NULL)''')

def pm_passwords():
    # Decalres commonly used variables and establishes the database comprised of a table with three columns.
    global conn 
    conn = sqlite3.connect("pm_passwords.db")
    global cursor 
    cursor = conn.cursor()

    conn.execute('''CREATE TABLE IF NOT EXISTS pm_passwords
        (username TEXT NOT NULL,
        website TEXT NOT NULL,
        password TEXT NOT NULL)''')

def create_acc():
    master_user = input("_" * 35 + "\n\nCreate Account:\n\nUsername: ").strip()
    master_pass = input("Master password: ").strip()
    confirm = input("Sign up for this account? (y/n): ").lower()

    while True:
        if confirm == 'y':
            user_input = (master_user, master_pass)
            sql = """INSERT INTO pm_accounts(master_user, master_pass) VALUES(?, ?)"""
            account_cursor.execute(sql, user_input)
            account_conn.commit()

            print("\nAccount successfully created." + "_" * 35)
            return True
        elif confirm == 'n':
            print("Returning to menu...")
            return False
        else:
            confirm = input("Invalid input, try again.\n: ")

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
            print("_" * 35 + "\n")
            return True
        else:
            print("Incorrect credentials.")
    else:
        return False

def options():
    # The main menu of the program that displays the commands to choose from.
    print("_" * 35)
    choice = input("""\nSelect from the following commands:
                   
Add new password (1)
Edit an existing password (2)
Delete an existing password (3)
Generate password (4)
Quit program (q)
                             
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
        elif choice == 'q':
            conn.close()
            print("\nConnection closed. Exiting program... ʕ •ᴥ•ʔ\n")
            quit()
        else:
            print('\nUndefined command, try again.')
            choice = input(": ")

def add_pass():
    # Receives three inputs and inserts them to the database.
    new_user = input("_" * 35 + "\n\nEnter new username or email: ").strip()
    new_web = input("Name of website or application: ").strip()
    user_input = (new_user, new_web)

    sql_check = """SELECT * FROM pm_passwords WHERE username = ? AND website = ?"""
    cursor.execute(sql_check, user_input)
    row = cursor.fetchone()

    if row:
        print("\nAn entry already exists with those exact inputs. ʕ ´•̥̥̥ ᴥ•̥̥̥`ʔ")
    else:
        new_pass = input("Enter new password: ").strip()
        user_input = (new_user, new_web, new_pass)
        sql = """INSERT INTO pm_passwords(username, website, password) VALUES(?, ?, ?)"""

        cursor.execute(sql, user_input)
        conn.commit()

        print("\nPassword successfully added. ＼ʕ •ᴥ•ʔ／")

    options()

def edit_pass(): 
    # Takes the username and website corresponding to a password and checks to see if they are present in the database. 
    # If so, user is asked to input the updated password, which is then updated in the database. 
    # Else, if the entry is not present, returns to menu.
    user_of_pass = input("_" * 35 + "\n\nEnter the username/email of the password that you would like to edit: ").strip()
    web_of_pass = input("Enter the website/app of the password that you would like to edit: ").strip()
    user_input = (user_of_pass, web_of_pass)

    sql_check = """SELECT * FROM pm_passwords WHERE username = ? AND website = ?"""
    cursor.execute(sql_check, user_input)
    row = cursor.fetchone()

    if row:
        # If entry exists, update the password.
        change_pass = input("Enter the updated password: ").strip()
        confirm = input("\nAre you sure you want to edit this entry? (y/n): ").lower()

        while True:
            if confirm == 'y':
                user_input = (change_pass, user_of_pass, web_of_pass)
                sql_update = """UPDATE pm_passwords SET password = ? WHERE username = ? AND website = ?"""   
                cursor.execute(sql_update, user_input)

                conn.commit()
                print("\nPassword successfully changed. ＼ʕ •ᴥ•ʔ／")
                break
            elif confirm == 'n':
                print("\nReturning back to menu...")
                break
            else:
                confirm = input("Invalid input, try again.\n:  ")
    else:
        print("\nEntry not found. No password updated. ʕ ´•̥̥̥ ᴥ•̥̥̥`ʔ")

    options()

def delete_pass():
    # Takes the username and website corresponding to a password and checks to see if they are present in the database. 
    # If so, user is asked whether or not that want to delete it.
    # Else, if the entry is not present, returns to menu.
    del_user = input("_" * 35 + "\n\nEnter the username/email of the password that you would like to delete: ").strip()
    del_web = input("Enter the website/app of the password that you would like to delete: ").strip()
    user_input = (del_user, del_web)

    sql_check = """SELECT * FROM pm_passwords WHERE username = ? AND website = ?"""
    cursor.execute(sql_check, user_input)
    row = cursor.fetchone()

    if row:
        confirm = input("\nAre you sure you want to delete this entry? (y/n): ").lower()
        while True:
            if confirm == 'y':
                sql = """DELETE FROM pm_passwords WHERE username = ? AND website = ?"""
                cursor.execute(sql, user_input)

                conn.commit()
                print("\nPassword successfully deleted. ＼ʕ •ᴥ•ʔ／")
                break
            elif confirm == 'n':
                print("\nReturning back to menu...")
                break
            else:
                confirm = input("Invalid input, try again.\n:  ")
    else:
        print("\nEntry not found. No password deleted. ʕ ´•̥̥̥ ᴥ•̥̥̥`ʔ")

    options()

def pass_gen():
    # Generates a random 32 character password and copies it to clipboard.
    char_set = string.ascii_letters + string.digits + string.punctuation
    password = ""

    for i in range(32):
        random_char = random.choice(char_set)
        password += random_char

    print("_" * 35 + "\n\nYour generated password:", password)

    while True:
        copy = input("Copy generated password to clipboard? (y/n): ").lower()
        if copy == 'y':
            pyperclip.copy(password)
            print("\nPassword successfully copied to clipboard. ＼ʕ •ᴥ•ʔ／")
            break
        elif copy == 'n':
            print("\nReturning to menu...")
            break
        else:
            copy = input("Invalid input, try again.\n: ")

    options()

main()