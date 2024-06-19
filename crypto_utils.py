import hashlib
from cryptography.fernet import Fernet

def hash_master_password(master_pass):
    # Hashes the master password before adding/updating 
    # it in the account credentials database.
    h = hashlib.new("SHA256")
    h.update(master_pass.encode())
    hashed_master_pass = h.hexdigest()
    return hashed_master_pass

def generate_fernet_key(current_user):
    # Generates a key and saves it into a file
    key = Fernet.generate_key()
    with open(f"{current_user}_secret.key", "wb") as key_file:
        key_file.write(key)

def load_fernet_key(current_user):
    # Loads the generated key
    with open(f"{current_user}_secret.key", "rb") as key_file:
        key = key_file.read()
    return key

def encrypt_password(password, current_user):
    # Encrypts a single password
    key = load_fernet_key(current_user)

    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, current_user):
    # Decrypts a single encrypted password
    key = load_fernet_key(current_user)

    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password.decode())
    return decrypted_password

def decrypt_password_entries(rows, current_user):
    # Decrypts all entries of the password manager database.
    decrypted_rows = []
    for row in rows:
        decrypted_pass = decrypt_password(row[2], current_user)
        decrypted_rows.append((row[0], row[1], decrypted_pass))
    return decrypted_rows