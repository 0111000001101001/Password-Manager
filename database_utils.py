import sqlite3, sys
from misc import confirm_user_input
from crypto_utils import hash_master_password
from crypto_utils import encrypt_password

def create_master_accounts_db():
    # Sets up a database for storing master account credentials.
    global account_conn, account_cursor
    account_conn = sqlite3.connect("password_manager.db")
    account_cursor = account_conn.cursor()
    account_conn.execute("""CREATE TABLE IF NOT EXISTS account_credentials
        (master_user TEXT NOT NULL,
        master_pass TEXT NOT NULL)""")

def create_password_manager_db(current_user):
    # Sets up the password manager database for a specific user, allowing them to store and manage their passwords.
    global conn, cursor
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    conn.execute(f"""CREATE TABLE IF NOT EXISTS passwords_{current_user}
        (website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL)""")

def add_account_to_db(user, password):
    # Takes in the master password of the newly created accounts and hashes it, then 
    # inserts the entry into the master account credentials database.
    hashed_master_password = hash_master_password(password)

    sql = "INSERT INTO account_credentials(master_user, master_pass) VALUES(?, ?)"
    account_cursor.execute(sql, (user, hashed_master_password))
    account_conn.commit()

def master_username_exists(user):
    # Checks to see if a master username already exists in database.
    sql = "SELECT * FROM account_credentials WHERE master_user = ?"
    account_cursor.execute(sql, (user,))
    return account_cursor.fetchone()

def verify_master_account_credentials(user, password):
    # Takes in the inputted master password, hashes it, then compares it to the already
    # hashed master password in the account credentials database.
    hashed_master_password = hash_master_password(password)

    sql = "SELECT * FROM account_credentials WHERE master_user = ? AND master_pass = ?"
    account_cursor.execute(sql, (user, hashed_master_password))
    return account_cursor.fetchone()

def entry_exists_in_db(current_user, cursor, website, username):
    # Checks to see whether or not a user input already exists in the database.
    sql = f"SELECT * FROM passwords_{current_user} WHERE website = ? AND username = ?"
    cursor.execute(sql, (website, username))
    if cursor.fetchone():
        return True
    else:
        return False
    
def add_password_to_db(current_user, website, username):
    # Inserts new entry into password manager database only if it does not already exist.
    if entry_exists_in_db(current_user, cursor, website, username):
        return True
    else:
        new_pass = input("Password: ").strip()

        encrypted_pass = encrypt_password(new_pass, current_user)

        sql = f"INSERT INTO passwords_{current_user}(website, username, password) VALUES(?, ?, ?)"
        cursor.execute(sql, (website, username, encrypted_pass))
        conn.commit()
        return False

def update_password_in_db(current_user, website, username):
    # Updates password only if the entry is found in the database.
    if entry_exists_in_db(current_user, cursor, website, username):
        changed_pass = input("Updated password: ").strip()
        confirm = input("\nAre you sure you want to edit this entry? (y/n): ").lower()

        if confirm_user_input(confirm):
            encrypted_pass = encrypt_password(changed_pass, current_user)

            sql = f"UPDATE passwords_{current_user} SET password = ? WHERE website = ? AND username = ?"
            cursor.execute(sql, (encrypted_pass, website, username))
            conn.commit()
            return "updated"
        else:
            return "cancelled"
    else:
        return "not_found"

def delete_password_from_db(user, website, username):
    # Deletes password only if the entry is found in the database.
    if entry_exists_in_db(user, cursor, website, username):
        confirm = input("\nAre you sure you want to delete this entry? (y/n): ").lower()
        
        if confirm_user_input(confirm):
            sql = f"DELETE FROM passwords_{user} WHERE website = ? AND username = ?"
            cursor.execute(sql, (website, username))
            conn.commit()
            return "deleted"
        else:
            return "cancelled"
    else:
        return "not_found"

def search_passwords_in_db(current_user, search_pass):
    # Allows users to search their password database by filtering website names that start with a given string.
    sql = f"SELECT * FROM passwords_{current_user} WHERE website LIKE ?"
    cursor.execute(sql, (search_pass,))
    return cursor.fetchall()

def get_all_passwords_from_db(current_user):
    # Selects all rows, rearranges in alphabetical order, and prints the table that stores the user's passwords.
    sql = f"SELECT * FROM passwords_{current_user} ORDER BY website ASC"
    cursor.execute(sql)
    return cursor.fetchall()

def update_master_password(user, password):
    # Takes in the updated master password, hashes it, then updates the entry in the account credentials database.
    hashed_master_password = hash_master_password(password)

    sql = "UPDATE account_credentials SET master_pass = ? WHERE master_user = ?"
    account_cursor.execute(sql, (hashed_master_password, user))
    account_conn.commit()

def close_master_accounts_db_and_exit():
    account_conn.close()
    sys.exit("\nExiting program... ʕ •ᴥ•ʔ\n")

def close_all_db_connections_and_exit():
    conn.close()
    account_conn.close()
    sys.exit("\nExiting program... ʕ •ᴥ•ʔ\n")