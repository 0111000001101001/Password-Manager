import getpass
import sqlite3

# To-do list:
# - Add 16 character random password generator and the ability to quickly copy it.
# - Add database encryption or store hashed version of passwords.
# - Remove the log-in credentials from the source code.
# - Implement more error-handling.

def main():
    print("\n\\\\\\Welcome to Password Manager///\n")

    # If authentication check was successful, the user is presented with commands to choose from.
    if pass_check():
        my_sql()
        options()
    else:
        print("Too many failed attempts, exiting program...")
        quit()

def my_sql():
    # Decalres commonly used variables and establishes the database comprised of a table with three columns.
    global conn 
    conn = sqlite3.connect("pm.db")
    global cursor 
    cursor = conn.cursor()

    conn.execute('''CREATE TABLE IF NOT EXISTS pass_manager
        (username TEXT NOT NULL,
        website TEXT NOT NULL,
        password TEXT NOT NULL)''')

def pass_check():
    correct_user = "admin"
    correct_pass = "adminpass"
    
    # Limited attempts to gain access to the program. Provides an authentication check.
    for i in range(5):
        user = input("Enter username: ")
        password = getpass.getpass("Enter password: ")

        if user == correct_user and password == correct_pass:
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
Quit program (q)
                             
Input: """).lower()

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
        elif choice == 'q':
            conn.close()
            print("Connection closed. Exiting program...")
            quit()
        else:
            print('\nUndefined command, try again.')
            choice = input(": ")    

def add_pass():
    # Receives three inputs and inserts them to the database.
    new_user = input("\nEnter the new username or email: ")
    new_web = input("Name of website or application: ")
    new_pass = input("Enter new password: ")

    sql = """INSERT INTO pass_manager(username, website, password) VALUES('{}', '{}', '{}')""".format(new_user, new_web, new_pass)

    cursor.execute(sql)
    conn.commit()

    print("Password successfully added.")
    options()

def edit_pass(): 
    # Takes the username and website corresponding to a password and checks to see if they are present in the database. 
    # If so, user is asked to input the updated password, which is then updated in the database. 
    # Else, if the entry is not present, returns to menu.
    user_of_pass = input("\nEnter the username/email of the password that you would like to edit: ")
    web_of_pass = input("Enter the website/app of the password that you would like to edit: ")

    sql_check = """SELECT * FROM pass_manager WHERE username = '{}' AND website = '{}' """.format(user_of_pass, web_of_pass)
    cursor.execute(sql_check)
    row = cursor.fetchone()

    if row:
        # If entry exists, update the password.
        new_pass = input("Enter the updated password: ")
        confirm = input("\nAre you sure you want to edit this entry? (y/n): ").lower()

        while True:
            if confirm == 'y':
                sql_update = """UPDATE pass_manager SET password = '{}' WHERE username = '{}' AND website = '{}' """.format(new_pass, user_of_pass, web_of_pass)
                cursor.execute(sql_update)
                conn.commit()
                print("Password successfully changed.")
                break
            elif confirm == 'n':
                print("Returning back to menu...")
                break
            else:
                confirm = input("Invalid input, try again.\n:  ")
    else:
        print("Entry not found. No password updated.")

    options()

def delete_pass():
    # Takes the username and website corresponding to a password and checks to see if they are present in the database. 
    # If so, user is asked whether or not that want to delete it.
    # Else, if the entry is not present, returns to menu.
    del_user = input("\nEnter the username/email of the password that you would like to delete: ")
    del_web = input("Enter the website/app of the password that you would like to delete: ")

    sql_check = """SELECT * FROM pass_manager WHERE username = '{}' AND website = '{}' """.format(del_user, del_web)
    cursor.execute(sql_check)
    row = cursor.fetchone()

    if row:
        confirm = input("\nAre you sure you want to delete this entry? (y/n): ").lower()
        while True:
            if confirm == 'y':
                sql = """DELETE FROM pass_manager WHERE username = '{}' AND website = '{}' """.format(del_user, del_web)
                cursor.execute(sql)
                conn.commit()
                print("Password successfully deleted.")
                break
            elif confirm == 'n':
                print("Returning back to menu...")
                break
            else:
                confirm = input("Invalid input, try again.\n:  ")
    else:
        print("Entry not found. No password deleted.")

    options()

main()