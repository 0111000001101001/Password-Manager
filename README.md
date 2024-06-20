# password-manager

### About:
A Python-based password manager, developed in VS Code, provides a secure and user-friendly way to store, manage, and generate passwords. It uses SQLite for database management and offers functionalities for creating, updating, deleting, and listing password entries. Additionally, SHA-256 is implemented to securely store master account credentials, and the "Cryptography" library is used to encrypt the vault of each user. As a beginner programmer, I made an attempt to implement conventional coding practices to improve readability, maintainability, and simplicity.

### Features:
- **Account Management:** Users can create master accounts and update master passwords.
- **Password Storage:** Users can store and manage their personal website or application passwords in a local SQLite database.
- **Cryptography:** Master passwords are hashed using SHA-256, and personal vaults are encrypted using the Fernet encryption library, ensuring that stored passwords are secure.
- **Search and Manage Entries:** Users can add, update, delete, search, and list all stored passwords.
- **Password Generation:** Generates random, 32-byte passwords for users.
- **User Interface:** A user-friendly command-line interface.

### Requirements:

- Cryptography
```
pip install cryptography
```
- Tabulate
```
pip install tabulate
```
- Pyperclip
```
pip install pyperclip
```

- VS Code - SQLite  Viewer extension
>Name: SQLite Viewer
>
>Id: qwtel.sqlite-viewer
>
>Description: SQLite Viewer for VSCode
>
>Version: 0.5.8
>
>Publisher: Florian Klampfer
>
>VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer

### Run the program:
```
python main.py
```

This is my first passion project, and I had a lot of fun working on it :)
