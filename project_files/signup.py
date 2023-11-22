# general purpose functions
import re
import sqlite3
import os
import customtkinter
from settings import set_value, get_value
# used for deriving
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
# used for encrypting
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
# used for changing frame
import login


class SignUp(customtkinter.CTkFrame):
    """The sign-up frame for our app."""

    def __init__(self, parent, controller):
        # variables
        self.data = {"username": None, "email": None, "phone": None, "password": None, "repeat_password": None}
        self.manipulated_data = {"password": b"", "salt_password": b"", "email": b"", "phone": b"", "salt_key": b""}
        self.incorrect_labels = []
        self.nonce = {"email": b"", "phone": b""}

        customtkinter.CTkFrame.__init__(self, parent)

        # labels, entries and buttons
        label = customtkinter.CTkLabel(self, text="Sign Up", font=("Impact", 25))
        label.grid(row=1, column=3, pady=(100, 5))

        specifications_username = customtkinter.CTkLabel(self, text="The username should be at least 6 characters "
                                                              "long and should only contain"
                                                              "numbers, letters, hyphens and underscores.",
                                                         font=("Arial", 15, 'bold'))
        specifications_username.grid(row=2, column=1, columnspan=5, pady=4, padx=(95, 100))
        username = customtkinter.CTkLabel(self, text="Username:", font=("Trebuchet MS", 16))
        username.grid(row=3, column=2, pady=2)
        entry_username = customtkinter.CTkEntry(self, placeholder_text="username", font=("Trebuchet MS", 15))
        entry_username.grid(row=3, column=4, pady=2)
        self.data["username"] = entry_username

        email = customtkinter.CTkLabel(self, text="Email:", font=("Trebuchet MS", 16))
        email.grid(row=4, column=2, pady=2)
        email_entry = customtkinter.CTkEntry(self, placeholder_text="email", font=("Trebuchet MS", 15))
        email_entry.grid(row=4, column=4, pady=2)
        self.data["email"] = email_entry

        phone = customtkinter.CTkLabel(self, text="Phone Number:", font=("Trebuchet MS", 16))
        phone.grid(row=5, column=2, pady=2)
        phone_entry = customtkinter.CTkEntry(self, placeholder_text="phone", font=("Trebuchet MS", 15))
        phone_entry.grid(row=5, column=4, pady=2)
        self.data["phone"] = phone_entry

        specifications_password = customtkinter.CTkLabel(self, text="The password should be at least 8 characters "
                                                              "long and should contain:\n a "
                                                              "number, a lowercase letter,"
                                                              "an uppercase letter and a special symbol "
                                                              "! # $ % & * + - , . : ; ? @ ~",
                                                         font=("Arial", 15, 'bold'))
        specifications_password.grid(row=6, column=1, columnspan=5, pady=(20, 4))

        password = customtkinter.CTkLabel(self, text="Password:", font=("Trebuchet MS", 16))
        password.grid(row=7, column=2, pady=2)
        entry_password = customtkinter.CTkEntry(self, placeholder_text="password", show="*", font=("Trebuchet MS", 15))
        entry_password.grid(row=7, column=4)
        self.data["password"] = entry_password

        repeat_password = customtkinter.CTkLabel(self, text="Repeat password:", font=("Trebuchet MS", 16))
        repeat_password.grid(row=8, column=2, pady=2)
        repeat_password_entry = customtkinter.CTkEntry(self, placeholder_text="password", show="*",
                                                       font=("Trebuchet MS", 15))
        repeat_password_entry.grid(row=8, column=4, pady=2)
        self.data["repeat_password"] = repeat_password_entry

        # format errors
        text_display = ["WRONG FORMAT USERNAME", "WRONG FORMAT EMAIL", "WRONG FORMAT PHONE", "WRONG FORMAT PASSWORD",
                        "PASSWORDS DO NOT MATCH", "USERNAME ALREADY EXISTS"]
        for item in text_display:
            format_label = customtkinter.CTkLabel(self, text=f"{item}", text_color="red")
            self.incorrect_labels.append(format_label)

        sign_up_button = customtkinter.CTkButton(self, text="Sign Up", text_color="#3E4B3C",
                        command=lambda: self.check_parameters(controller, self.incorrect_labels),
                        fg_color="#91D53E", hover_color="#689F33", border_color="#3E4B3C", height=30, border_width=1)
        sign_up_button.grid(row=9, column=3)

        return_menu = customtkinter.CTkButton(self, text="RETURN TO LOGIN PAGE", text_color="WHITE",
                        command=lambda: controller.show_frame(login.Login),
                        fg_color="#91D53E", hover_color="#689F33", border_color="WHITE", height=30, border_width=1)
        return_menu.grid(row=10, column=3, pady=5)

    def check_parameters(self, controller, incorrect_labels):
        """This functions will check the data using the parameters established.
        If the data is correct it will call register_user, if not it will display a red warning label."""
        regex_username = r"^[a-zA-Z0-9_-]{6,}$"
        regex_password = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!#$%&*+_,.:;?@~]).{8,}$"
        regex_email = r"^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$"
        regex_phone = r"^[0-9]{9}$"

        for item in self.incorrect_labels:
            item.grid_remove()

        if re.fullmatch(regex_username, self.data["username"].get()) is None:
            incorrect_labels[0].grid(row=11, column=3)

        elif re.fullmatch(regex_email, self.data["email"].get()) is None:
            incorrect_labels[1].grid(row=11, column=3)

        elif re.fullmatch(regex_phone, self.data["phone"].get()) is None:
            incorrect_labels[2].grid(row=11, column=3)

        elif re.fullmatch(regex_password, self.data["password"].get()) is None:
            incorrect_labels[3].grid(row=11, column=3)
        elif self.data["password"].get() != self.data["repeat_password"].get():
            incorrect_labels[4].grid(row=11, column=3)
        else:

            self.register_user(controller, incorrect_labels)

    def register_user(self, controller, incorrect_labels):
        """This function will register the user.
        If the username already exists it will display a red warning label."""
        # sql initialize
        cwd = os.getcwd()
        sqlite_file = cwd + r"/project_files/database_project.db"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()
        # create table
        sql = ("create table if not exists users "
               "(username TEXT not null constraint users_pk primary key, password BLOB not null,"
               "email BlOB not null, phone_number BLOB not null,"
               "salt_password BLOB not null, nonce_email BLOB not null, salt_key BlOB not null,"
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
            # set the global username value
            set_value(self.data["username"].get())
            # derive and encrypt items
            self.derive_password()
            self.encrypt_data()
            # insert into table and log user
            sql = """INSERT INTO users (username, email, phone_number, 
            password, salt_password, nonce_email, nonce_phone_number, salt_key) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

            cursor.execute(sql,
                           [self.data["username"].get(), self.manipulated_data["email"],
                            self.manipulated_data["phone"], self.manipulated_data["password"],
                            self.manipulated_data["salt_password"], self.nonce["email"], self.nonce["phone"],
                            self.manipulated_data["salt_key"]])

            conn.commit()
            cursor.close()

            # write message in log
            messages = [f"Signup information for user: {get_value()}",
                        "Successfully encrypted and derived user data.",
                        "Algorithms used: ChaCha20, Scrypt. Length of key: 32\n"]
            controller.write_log(messages)

            # remove text from entries
            for item in self.data.values():
                item.delete(0, "end")
            # show main page
            controller.show_frame(login.Login)

    def derive_password(self):
        """This function will generate a salt and KDF to derive the user's password."""
        salt = os.urandom(32)

        derived_password = self.run_scrypt(salt)
        self.manipulated_data["password"] = derived_password
        self.manipulated_data["salt_password"] = salt

        return None

    def run_scrypt(self, salt):
        """This function will derive the password using the Scrypt function."""
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2 ** 14,
            r=8,
            p=1,
        )
        # derive password

        return kdf.derive(self.data["password"].get().encode())

    def encrypt_data(self):
        """This function will generate a nonce for each encrypted item (3) and then encrypt said items."""
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

        # initialize ChaCha
        chacha = ChaCha20Poly1305(key)

        for item in self.nonce.keys():
            encrypted_item = chacha.encrypt(self.nonce[f"{item}"], self.data[f"{item}"].get().encode(), None)
            self.manipulated_data[f"{item}"] = encrypted_item


