import sqlite3

def create_master_accounts_db():
    global account_conn, account_cursor
    account_conn = sqlite3.connect("password_manager.db")
    account_cursor = account_conn.cursor()
    account_conn.execute("""CREATE TABLE IF NOT EXISTS account_credentials
        (master_user TEXT NOT NULL,
        master_pass TEXT NOT NULL)""")

def create_password_manager_db(current_user):
    global conn, cursor
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()
    conn.execute(f"""CREATE TABLE IF NOT EXISTS passwords_{current_user}
        (website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL)""")

def add_account_to_db(user, password):
    sql = "INSERT INTO account_credentials(master_user, master_pass) VALUES(?, ?)"
    account_cursor.execute(sql, (user, password))
    account_conn.commit()

def master_username_exists(user):
    sql = "SELECT * FROM account_credentials WHERE master_user = ?"
    account_cursor.execute(sql, (user,))
    return account_cursor.fetchone()

def verify_master_account_credentials(user, password):
    sql = "SELECT * FROM account_credentials WHERE master_user = ? AND master_pass = ?"
    account_cursor.execute(sql, (user, password))
    return account_cursor.fetchone()

def entry_exists_in_db(user, cursor, website, username):
    sql = f"SELECT * FROM passwords_{user} WHERE website = ? AND username = ?"
    cursor.execute(sql, (website, username))
    if cursor.fetchone():
        return True
    else:
        return False
    
def add_password_to_db(current_user, website, username):
    if entry_exists_in_db(current_user, cursor, website, username):
        return True
    else:
        new_pass = input("Password: ").strip()

        sql = f"INSERT INTO passwords_{current_user}(website, username, password) VALUES(?, ?, ?)"
        cursor.execute(sql, (website, username, new_pass))
        conn.commit()
        return False

def update_password_in_db(current_user, website, username):
    if entry_exists_in_db(current_user, cursor, website, username):
        changed_pass = input("Updated password: ").strip()

        confirm = input("\nAre you sure you want to edit this entry? (y/n): ").lower()
        while True:
            if confirm == 'y':
                sql = f"UPDATE passwords_{current_user} SET password = ? WHERE website = ? AND username = ?"
                cursor.execute(sql, (changed_pass, website, username))
                conn.commit()
                return "updated"
            elif confirm == 'n':
                return "cancelled"
            else:
                confirm = input("\nInvalid input, try again.\n: ").lower()
    else:
        return "not_found"

def delete_password_from_db(user, website, username):
    if entry_exists_in_db(user, cursor, website, username):
        confirm = input("\nAre you sure you want to delete this entry? (y/n): ").lower()
        while True:
            if confirm == 'y':
                sql = f"DELETE FROM passwords_{user} WHERE website = ? AND username = ?"
                cursor.execute(sql, (website, username))
                conn.commit()
                return "deleted"
            elif confirm == 'n':
                return "cancelled"
            else:
                confirm = input("\nInvalid input, try again.\n: ").lower()
    else:
        return "not_found"

def search_passwords_in_db(current_user, search_pass):
    sql = f"SELECT * FROM passwords_{current_user} WHERE website LIKE ?"
    cursor.execute(sql, (search_pass,))
    return cursor.fetchall()

def get_all_passwords_from_db(current_user):
    sql = f"SELECT * FROM passwords_{current_user} ORDER BY website ASC"
    cursor.execute(sql)
    return cursor.fetchall()

def update_master_password(user, new_password):
    sql = "UPDATE account_credentials SET master_pass = ? WHERE master_user = ?"
    account_cursor.execute(sql, (new_password, user))
    account_conn.commit()