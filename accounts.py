def validate_username(username):
     # Checks to see if the inputted username is comprised of only letters and numbers, 
    # and has a minimum length of 3 characters and a maximum of 16.
    return username.isalnum() and 3 <= len(username) <= 16

def validate_password(password):
    # Password must be at least 8 characters, and have max character count of 128.
    return 8 <= len(password) <= 128