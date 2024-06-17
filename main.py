import sys
from database_utils import create_master_accounts_db, create_password_manager_db
from account_operations import create_master_account, authenticate_log_in
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
    
    create_master_accounts_db()

    while True:        
        if account_menu_input == '1':
            current_user = create_master_account()
            if current_user:
                create_password_manager_db(current_user)
                break
            else:
                sys.exit("\nExiting program... ʕ •ᴥ•ʔ\n")

        elif account_menu_input == '2':
            current_user = authenticate_log_in()
            if current_user:
                create_password_manager_db(current_user)
                break
            else:
                sys.exit("\nToo many failed attempts, exiting program... ʕ •ᴥ•ʔ\n")

        elif account_menu_input == 'q':
            sys.exit("\nExiting program... ʕ •ᴥ•ʔ\n")
        
        else:
            account_menu_input = input("\nInvalid input, try again.\n: ")
            continue

    while True:
        menu_options(current_user)

if __name__ == "__main__":
    main()