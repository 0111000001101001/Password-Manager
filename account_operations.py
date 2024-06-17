import getpass
from database_utils import add_account_to_db, verify_master_account_credentials
from validation_utils import get_valid_master_username, get_valid_master_password
from misc import confirm_user_input

def create_master_account():
    print("_" * 35 + "\n\nCreate Account:")

    master_user = get_valid_master_username()
    master_pass = get_valid_master_password()

    confirm = input("Sign up for this account? (y/n): ").lower()
    # Inserts the newly created account into the table and declares current_user of the program by returning master_user.
    if confirm_user_input(confirm):
        add_account_to_db(master_user, master_pass)
        print("\nAccount successfully created. ＼ʕ •ᴥ•ʔ／\n")
        return master_user
    else:
        return None

def authenticate_log_in():
    # Limited attempts to gain access to the program. Provides an authentication check and declaries current_user by returning exist_user
    for i in range(5):
        exist_user = input("_" * 35 + "\n\nLog-in:\n\nUsername: ").strip()
        exist_pass = getpass.getpass("Master password: ").strip()

        if verify_master_account_credentials(exist_user, exist_pass):
            return exist_user
        else:
            print("\nIncorrect credentials.")
    else:
        return None