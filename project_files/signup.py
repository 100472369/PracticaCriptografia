import re
import sqlite3
import os
import customtkinter
from mainpage import MainPage
from settings import set_value, set_encryption_key
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import login


class SignUp(customtkinter.CTkFrame):
    """The sign-up frame for our app."""

    def __init__(self, parent, controller):
        # variables
        self.data = {"username": None, "email": None, "phone": None, "password": None, "repeat_password": None}
        self.manipulated_data = {"password": None, "salt_password": None, "email": None, "phone": None, "salt_key": None}
        self.incorrect_labels = []
        self.nonce = {"email": None, "phone": None}

        customtkinter.CTkFrame.__init__(self, parent)

        # labels, entries and buttons
        label = customtkinter.CTkLabel(self, text="Sign Up", font=("Impact", 20))
        label.grid(row=1, column=4)

        specifications_username = customtkinter.CTkLabel(self,
                                                         text="The username should be at least 6 characters "
                                                              "long and should only contain "
                                                              "numbers, letters, hyphens and underscores.")
        specifications_username.grid(row=2, column=1, columnspan=7)
        username = customtkinter.CTkLabel(self, text="username:")
        username.grid(row=3, column=3)
        entry_username = customtkinter.CTkEntry(self, placeholder_text="username")
        entry_username.grid(row=3, column=5)
        self.data["username"] = entry_username

        email = customtkinter.CTkLabel(self, text="email:")
        email.grid(row=4, column=3)
        email_entry = customtkinter.CTkEntry(self, placeholder_text="email")
        email_entry.grid(row=4, column=5)
        self.data["email"] = email_entry

        phone = customtkinter.CTkLabel(self, text="phone number:")
        phone.grid(row=5, column=3)
        phone_entry = customtkinter.CTkEntry(self, placeholder_text="phone")
        phone_entry.grid(row=5, column=5)
        self.data["phone"] = phone_entry

        specifications_password = customtkinter.CTkLabel(self,
                                                         text="                 "
                                                              "The password should be at least 8 characters "
                                                              "long and should contain: a "
                                                              "number, a lowercase letter, "
                                                              "an uppercase letter and a special symbol "
                                                              "! # $ % & * + - , . : ; ? @ ~")
        specifications_password.grid(row=6, column=1, columnspan=7)

        password = customtkinter.CTkLabel(self, text="password:")
        password.grid(row=7, column=3)
        entry_password = customtkinter.CTkEntry(self, placeholder_text="password", show="*")
        entry_password.grid(row=7, column=5)
        self.data["password"] = entry_password

        repeat_password = customtkinter.CTkLabel(self, text="repeat password:")
        repeat_password.grid(row=8, column=3)
        repeat_password_entry = customtkinter.CTkEntry(self, placeholder_text="password", show="*")
        repeat_password_entry.grid(row=8, column=5)
        self.data["repeat_password"] = repeat_password_entry

        # format errors
        text_display = ["WRONG FORMAT USERNAME", "WRONG FORMAT EMAIL", "WRONG FORMAT PHONE", "WRONG FORMAT PASSWORD",
                        "PASSWORDS DO NOT MATCH", "USERNAME ALREADY EXISTS"]
        for item in text_display:
            format_label = customtkinter.CTkLabel(self, text=f"{item}", text_color="red")
            self.incorrect_labels.append(format_label)

        sign_up_button = customtkinter.CTkButton(self, text="Sign Up",
                                                 command=lambda: self.check_parameters(controller,
                                                                                       self.incorrect_labels))
        sign_up_button.grid(row=9, column=4)

        return_menu = customtkinter.CTkButton(self, text="RETURN TO LOGIN PAGE",
                                              command=lambda: controller.show_frame(login.Login))
        return_menu.grid(row=10, column=4, pady=5)

    def check_parameters(self, controller, incorrect_labels):
        """This functions will check the parameters established.
        If iot does it will call register_user, if not it will display a red warning label."""
        regex_username = "^[a-zA-Z0-9_-]{6,}$"
        regex_password = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!#$%&*+_,.:;?@~]).{8,}$"
        regex_email = "^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$"
        regex_phone = "^[0-9]{9}$"

        for item in self.incorrect_labels:
            item.grid_remove()

        if re.fullmatch(regex_username, self.data["username"].get()) is None:
            incorrect_labels[0].grid(row=11, column=4)

        elif re.fullmatch(regex_email, self.data["email"].get()) is None:
            incorrect_labels[1].grid(row=11, column=4)

        elif re.fullmatch(regex_phone, self.data["phone"].get()) is None:
            incorrect_labels[2].grid(row=11, column=4)

        elif re.fullmatch(regex_password, self.data["password"].get()) is None:
            incorrect_labels[3].grid(row=11, column=4)
        elif self.data["password"].get() != self.data["repeat_password"].get():
            incorrect_labels[4].grid(row=11, column=4)
        else:

            self.register_user(controller, incorrect_labels)

    def register_user(self, controller, incorrect_labels):
        """This function will register the user.
        If the username exists it will display a red warning label."""
        # sql initialize
        cwd = os.getcwd()
        sqlite_file = cwd + r"/project_files/database_project.db"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()
        # create table
        sql = ("create table if not exists users "
               "(username TEXT not null constraint users_pk primary key, password BLOB not null,"
               "email BlOB not null, phone_number BLOB not null,"
               "salt BLOB not null, nonce_email BLOB not null,"
               "nonce_phone_number BLOB not null);")
        cursor.execute(sql)

        # first check if username exists

        sql = "select username from users where username=?"
        cursor.execute(sql, [self.data["username"].get()])

        username = cursor.fetchall()
        if len(username) > 0:
            for item in self.incorrect_labels:
                item.grid_remove()
            incorrect_labels[5].grid(row=11, column=4)

        else:
            # derive and encrypt items
            self.derive_password()
            self.encrypt_data()

            # insert into table and log user
            sql = """INSERT INTO users (username, email, phone_number, password, salt_password, nonce_email, nonce_phone_number, salt_key) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

            cursor.execute(sql,
                           [self.data["username"].get(), self.manipulated_data["email"],
                            self.manipulated_data["phone"], self.manipulated_data["password"],
                            self.manipulated_data["salt_password"], self.nonce["email"], self.nonce["phone"],
                            self.manipulated_data["salt_key"]])

            conn.commit()
            cursor.close()

            set_value(self.data["username"].get())

            # remove text from entries
            for item in self.data.values():
                item.delete(0, "end")
            # show main page
            controller.show_frame(MainPage)

    def derive_password(self):
        """This function will generate a salt and KDF to derive the user's password."""
        salt = os.urandom(32)

        derived_password = self.run_scrypt(salt)
        self.manipulated_data["password"] = derived_password
        self.manipulated_data["salt_password"] = salt

        return None

    def run_scrypt(self, salt):
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2 ** 14,
            r=8,
            p=1,
        )
        # encrypt password

        return kdf.derive(self.data["password"].get().encode())

    def encrypt_data(self):
        """This function will generate a nonce for each encrypted item (3) and will encrypt said items"""
        # get global key
        salt = os.urandom(32)
        key = self.run_scrypt(salt)
        # insert salt into manipulated data
        self.manipulated_data["salt_key"] = salt

        # create the 2 nonce's for each encryption
        # email
        self.nonce["email"] = os.urandom(12)
        # phone
        self.nonce["phone"] = os.urandom(12)

        # initialize chacha
        chacha = ChaCha20Poly1305(key)

        keys = list(self.nonce.keys())

        i = 0
        for item in self.nonce.values():
            encrypted_item = chacha.encrypt(self.nonce[f"{item}"], self.data[f"{keys[i]}"].get().encode(), None)
            self.manipulated_data[f"{keys[i]}"] = encrypted_item
            i += 1

        # store key as temporary global variable
        set_encryption_key(key)

