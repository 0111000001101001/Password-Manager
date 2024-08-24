import sqlite3, sys
from crypto import hash_master_password, encrypt_entry
from misc import confirm_user_input

def init_master_accounts_db():
    # initializes the database for storing master account credentials.
    global account_conn, account_cursor
    account_conn = sqlite3.connect("password_manager.db")
    account_cursor = account_conn.cursor()
    account_conn.execute("""CREATE TABLE IF NOT EXISTS account_credentials
        (master_user TEXT NOT NULL,
        master_pass TEXT NOT NULL)""")

def init_password_manager_db(current_user):
    # initializes the personal vault of the current_user, allowing them to store and manage their passwords.
    global conn, cursor
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    conn.execute(f"""CREATE TABLE IF NOT EXISTS passwords_{current_user}
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL)""")

def add_account_to_db(username, password):
    # Takes in the master password of the newly created accounts and hashes it, then 
    # inserts the entry into the master account credentials database.
    hashed_master_password = hash_master_password(password)

    sql = "INSERT INTO account_credentials(master_user, master_pass) VALUES(?, ?)"
    account_cursor.execute(sql, (username, hashed_master_password))
    account_conn.commit()

def master_username_exists(username):
    # Checks to see if a master username already exists in database.
    sql = "SELECT * FROM account_credentials WHERE master_user = ?"
    account_cursor.execute(sql, (username,))
    return account_cursor.fetchone()

def verify_master_account_credentials(username, password):
    # Takes in the inputted master password, hashes it, then compares it to the already
    # hashed master password in the account credentials database.
    hashed_master_password = hash_master_password(password)

    sql = "SELECT * FROM account_credentials WHERE master_user = ? AND master_pass = ?"
    account_cursor.execute(sql, (username, hashed_master_password))
    return account_cursor.fetchone()

def entry_exists_in_db(current_user, cursor, entry_id):
    # Checks to see whether or not the entry_id exists in the database.
    sql = f"SELECT * FROM passwords_{current_user} WHERE id = ?"
    cursor.execute(sql, (entry_id,))
    if cursor.fetchone():
        return True
    else:
        return False
    
def add_password_to_db(current_user, website, username, password):
    # Encrypts new entry and inserts into the current_user's vault.
    encrypted_user = encrypt_entry(current_user, username)
    encrypted_pass = encrypt_entry(current_user, password)

    sql = f"INSERT INTO passwords_{current_user}(website, username, password) VALUES(?, ?, ?)"
    cursor.execute(sql, (website, encrypted_user, encrypted_pass))
    conn.commit()

def update_password_in_db(current_user, entry_id):
    # If the entry is found, encrypts the updated password and replaces it with the existing password.
    if entry_exists_in_db(current_user, cursor, entry_id):
        changed_pass = input("Updated password: ")
        confirm = input("\nAre you sure you want to edit this entry? (y/n): ").lower()

        if confirm_user_input(confirm):
            encrypted_pass = encrypt_entry(current_user, changed_pass)

            sql = f"UPDATE passwords_{current_user} SET password = ? WHERE id = ?"
            cursor.execute(sql, (encrypted_pass, entry_id))
            conn.commit()
            return "updated"
        else:
            return "cancelled"
    else:
        return "not_found"

def delete_password_from_db(current_user, entry_id):
    # Deletes password only if the entry is found in the database.
    if entry_exists_in_db(current_user, cursor, entry_id):
        confirm = input("\nAre you sure you want to delete this entry? (y/n): ").lower()
        
        if confirm_user_input(confirm):
            sql = f"DELETE FROM passwords_{current_user} WHERE id = ?"
            cursor.execute(sql, (entry_id,))
            conn.commit()
            return "deleted"
        else:
            return "cancelled"
    else:
        return "not_found"

def search_passwords_in_db(current_user, website):
    # Allows users to search their password database by filtering website names that start with a given string.
    sql = f"SELECT * FROM passwords_{current_user} WHERE website LIKE ?"
    cursor.execute(sql, (website,))
    return cursor.fetchall()

def get_all_passwords_from_db(current_user):
    # Selects all rows, rearranges in alphabetical order and fetches all entries.
    sql = f"SELECT * FROM passwords_{current_user} ORDER BY website ASC"
    cursor.execute(sql)
    return cursor.fetchall()

def update_master_password(username, password):
    # Takes in the updated master password, hashes it, then updates the entry in the master account credentials database.
    hashed_master_password = hash_master_password(password)

    sql = "UPDATE account_credentials SET master_pass = ? WHERE master_user = ?"
    account_cursor.execute(sql, (hashed_master_password, username))
    account_conn.commit()

def close_master_accounts_db_and_exit():
    account_conn.close()
    sys.exit("\nExiting program... ʕ •ᴥ•ʔ\n")

def close_db_conns_and_exit():
    conn.close()
    account_conn.close()
    sys.exit("\nExiting program... ʕ •ᴥ•ʔ\n")