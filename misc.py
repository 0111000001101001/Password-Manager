def confirm_user_input(confirm):
    # Provides an authentication for carrying out certain actions.
    while True:
        if confirm == 'y':
            return True
        elif confirm == 'n':
            return False
        else:
            confirm = input("Invalid input, try again.\n: ").lower()