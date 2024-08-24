from database import master_username_exists

def get_valid_master_username():
    while True:
        # Checks to see if the inputted master username is comprised of only letters and numbers, 
        # with a minimum length of 5 characters and a maximum of 16.
        master_user = input("\nUsername: ")
        if not master_user.isalnum() or not 5 <= len(master_user) <= 16:
            print("Usernames can only contain letters and numbers with a minimum length of 5 characters and a maximum length of 16. Try again.")
            continue

        if master_username_exists(master_user):
            print("This username seems to be taken. Try entering a different one.")
            continue
        else:
            print("Username is available.\n")
            return master_user

def get_valid_master_password():
    # Checks that the password is at least 8 characters long and less than 128 characters long.
    while True:
        master_pass = input("Master password: ")
        if 8 <= len(master_pass) <= 128:
            return master_pass
        else:
            print("Master password needs to be at least 8 characters long with a limit of 128 characters. Try again.\n")
            continue