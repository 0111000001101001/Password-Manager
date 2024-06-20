import sys
from database_utils import init_master_accounts_db, init_password_manager_db, close_master_accounts_db_and_exit
from account_operations import create_master_account, authenticate_log_in
from crypto_utils import generate_fernet_key
from menu import menu_options

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

: """).lower().strip()
    
    init_master_accounts_db()

    while True:        
        if account_menu_input == '1':
            current_user = create_master_account()
            if current_user:
                init_password_manager_db(current_user)
                generate_fernet_key(current_user)
                break
            else:
                close_master_accounts_db_and_exit()

        elif account_menu_input == '2':
            current_user = authenticate_log_in()
            if current_user:
                init_password_manager_db(current_user)
                break
            else:
                print("Too many failed attempts.")
                close_master_accounts_db_and_exit()

        elif account_menu_input == 'q':
            close_master_accounts_db_and_exit()
        
        else:
            account_menu_input = input("\nInvalid input, try again.\n: ").lower().strip()

    while True:
        menu_options(current_user)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nAn error has occured: {e}")
        sys.exit(1)