# Password-Manager

### About:
A Python-based password manager, developed in VS Code, provides a secure way to locally store, manage, and generate passwords. It uses SQLite for database management and offers functionalities for creating, updating, deleting, and listing password entries. Additionally, SHA-512 is implemented to securely store master account credentials, and the "Cryptography" library is used to encrypt the vault of each user.

### Features:
- **Account Management:** Users can create master accounts and update master passwords.
- **Password Storage:** Users can store and manage their personal website or application passwords in a local SQLite database.
- **Cryptography:** Master passwords are hashed using SHA-512, and personal vaults are encrypted using the Fernet encryption library.
- **Search and Manage Entries:** Users can add, update, delete, search, and list all stored passwords.
- **Password Generation:** Generates random, 32-byte passwords for users.

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

- Made use of the SQLite Viewer extension to read the generated database, however, it is not required for this program.
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

### Clone repository:
```
https://github.com/0111000001101001/Password-Manager.git
```
### Run the program:
```
python main.py
```

This is my first passion project, and I had a lot of fun working on it :)

### Preview:
<img src="https://github.com/user-attachments/assets/be0a5742-f461-443a-bd82-8381010d883c" alt="PMExample1" width="700"/>
<img src="https://github.com/user-attachments/assets/d2fd686f-8022-4c96-9651-49340b8177ba" alt="PMExample2" width="415"/>
<img src="https://github.com/user-attachments/assets/9c2f2963-b606-4ed6-b851-73dc7039b159" alt="PMExample3" width="500"/>
<img src="https://github.com/user-attachments/assets/49a5fb08-f440-4cc9-a533-152a0e1d9def" alt="PMExample4" width="500"/>
