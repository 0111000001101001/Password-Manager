import getpass
from database_utils import add_account_to_db, verify_master_account_credentials
from validation_utils import get_valid_master_username, get_valid_master_password

def create_master_account():
    print("_" * 35 + "\n\nCreate Account:")

    master_user = get_valid_master_username()
    master_pass = get_valid_master_password()

    confirm = input("Sign up for this account? (y/n): ").lower()
    while True:
        # Inserts the newly created account into the table. And declares the current user of the program.
        if confirm == 'y':
            add_account_to_db(master_user, master_pass)
            print("\nAccount successfully created. ＼ʕ •ᴥ•ʔ／\n\n" + "_" * 35)
            return master_user
        elif confirm == 'n':
            return None
        else:
            confirm = input("Invalid input, try again.\n: ").lower()

def authenticate_log_in():
    for i in range(5):
        exist_user = input("_" * 35 + "\n\nLog-in:\n\nUsername: ").strip()
        exist_pass = getpass.getpass("Master password: ").strip()

        if verify_master_account_credentials(exist_user, exist_pass):
            return exist_user
        else:
            print("\nIncorrect credentials.")
    else:
        return None