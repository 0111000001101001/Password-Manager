import hashlib
from cryptography.fernet import Fernet

def hash_master_password(master_pass):
    # Hashes the master password before adding/updating 
    # it in the account credentials database.
    h = hashlib.new("SHA512")
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

def encrypt_entry(current_user, entry):
    # Encrypts a single entry
    key = load_fernet_key(current_user)

    f = Fernet(key)
    encrypted_entry = f.encrypt(entry.encode())
    return encrypted_entry

def decrypt_entry(current_user, encrypted_entry):
    # Decrypts a single encrypted entry
    key = load_fernet_key(current_user)

    f = Fernet(key)
    decrypted_entry = f.decrypt(encrypted_entry.decode())
    return decrypted_entry

def decrypt_all_entries(current_user, rows):
    # Decrypts all entries of the current_user's password vault.
    decrypted_rows = []
    for row in rows:
        decrypted_user = decrypt_entry(current_user, row[2])
        decrypted_pass = decrypt_entry(current_user, row[3])
        decrypted_rows.append((row[0], row[1], decrypted_user, decrypted_pass))
    return decrypted_rows
