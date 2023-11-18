import sqlite3
import os

import cryptography.exceptions
import customtkinter
from signup import SignUp
from mainpage import MainPage
from settings import set_value, set_encryption_key, get_value
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
# used for signature verification
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class Login(customtkinter.CTkFrame):
    """This is the login frame for our app."""
    def __init__(self, parent, controller):
        # variables
        self.data = []

        customtkinter.CTkFrame.__init__(self, parent)
        # this is used to center all the elements
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(4, weight=2)

        # labels, entries and buttons

        label = customtkinter.CTkLabel(self, text="Login Page", font=("Impact", 25))
        label.grid(row=1, column=2, pady=(155, 5))

        label_username = customtkinter.CTkLabel(self, text="Username:", font=("Trebuchet MS", 15))
        label_username.grid(row=2, column=1, pady=5)

        entry_username = customtkinter.CTkEntry(self, placeholder_text="username", font=("Trebuchet MS", 15))
        entry_username.grid(row=2, column=2, pady=5)
        self.data.append(entry_username)

        label_password = customtkinter.CTkLabel(self, text="Password: ", font=("Trebuchet MS", 15))
        label_password.grid(row=3, column=1, pady=2)

        entry_password = customtkinter.CTkEntry(self, placeholder_text="password", show="*", font=("Trebuchet MS", 15))
        entry_password.grid(row=3, column=2, pady=2)
        self.data.append(entry_password)

        login_button = customtkinter.CTkButton(self, text="Login", text_color="#3E4B3C", command=lambda: self.log_user
            (controller, incorrect_data), fg_color="#91D53E", hover_color="#689F33", border_color="#3E4B3C", height=30,
                                               border_width=1)
        login_button.grid(row=4, column=2, pady=2)

        sign_up_button = customtkinter.CTkButton(self, text="Sign up", text_color="#3E4B3C",
                                                 command=lambda: controller.show_frame(SignUp),
                                                 fg_color="#91D53E", hover_color="#689F33", border_color="#3E4B3C",
                                                 height=30, border_width=1)
        sign_up_button.grid(row=5, column=2, pady=2)

        incorrect_data = customtkinter.CTkLabel(self, text="INCORRECT USERNAME OR PASSWORD", text_color="red")

    def log_user(self, controller, label):
        """this function will try to log the user and redirect to the main page.
        If not possible it wil display a red label error."""

        # initiate sql data
        cwd = os.getcwd()
        sqlite_file = cwd + r"/project_files/database_project.db"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()

        # execute query
        sql = "select username, password, salt_password, salt_key FROM users where username=?"
        cursor.execute(sql, [self.data[0].get()])

        # user verification with sql data
        database_tuple = cursor.fetchall()

        if len(database_tuple) == 0:
            label.grid(row=6, column=1, columnspan=2)
            return None

        try:
            salt = database_tuple[0][2]
            kdf = self.generate_kdf(salt)

            kdf.verify(self.data[1].get().encode(), database_tuple[0][1])
        except cryptography.exceptions.InvalidKey:
            label.grid(row=6, column=1, columnspan=2)

        else:
            # set username value
            set_value(self.data[0].get())
            self.verify_signature(cursor, controller)
            # close cursor set the username value and show main page.
            cursor.close()
            # remove text from entries
            for item in self.data:
                item.delete(0, "end")
            # create key for accessing data
            salt = database_tuple[0][3]
            kdf = self.generate_kdf(salt)

            # store key as temporary global variable
            key = kdf.derive(self.data[1].get().encode())
            set_encryption_key(key)

            #  write message in log

            messages = [f"Login information for user: {get_value()}",
                        "Successfully verified user data.", "Algorithm used: Scrypt. Length of key: 32\n"]
            controller.write_log(messages)

            # show main page
            controller.show_frame(MainPage)

    def generate_kdf(self, salt):
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2 ** 14,
            r=8,
            p=1,
        )
        return kdf

    def verify_signature(self, cursor, controller):
        sql = """select username, public_key, signature from signature where username=?;"""
        cursor.execute(sql, [get_value()])
        data = cursor.fetchone()
        message = data[0].encode(encoding="UTF-8")
        public_key = load_pem_public_key(data[1])
        signature = data[2]
        try:
            public_key.verify(signature,
                              message,
                              padding.PSS(
                                  mgf=padding.MGF1(hashes.SHA256()),
                                  salt_length=padding.PSS.MAX_LENGTH
                              ),
                              hashes.SHA256()
            )
            messages = [f"Login information for user: {get_value()}",
                        "Successfully verified signature.", "Algorithm used: RSA. \n"]
            controller.write_log(messages)

            # show main page
            controller.show_frame(MainPage)
        except cryptography.exceptions.InvalidSignature:
            messages = [f"Login information for user: {get_value()}",
                        "Signature verification failed.",
                        "Check if user has signature entry in signature table of database. \n"]
            controller.write_log(messages)
