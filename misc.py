def confirm_user_input(confirm):
    # Provides an authentication for carrying out certain actions.
    while True:
        if confirm == 'y':
            return True
        elif confirm == 'n':
            return False
        else:
            confirm = input("Invalid input, try again.\n: ").lower().strip()

def return_to_menu():
    # Function is called after printing password entries.
    menu = input("_" * 35 + "\n\nResults are printed. Press 'm' to return to menu: ").lower().strip()
    while True:
        if menu == 'm':
            return
        else:
            menu = input("\nInvalid input, try again.\n: ").lower().strip()