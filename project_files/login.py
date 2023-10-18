import sqlite3
import os

import cryptography.exceptions
import customtkinter
from signup import SignUp
from mainpage import MainPage
from settings import set_value
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


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
        label = customtkinter.CTkLabel(self, text="Login Page")
        label.grid(row=1, column=2)

        label_username = customtkinter.CTkLabel(self, text="Username:")
        label_username.grid(row=2, column=1)

        entry_username = customtkinter.CTkEntry(self, placeholder_text="username")
        entry_username.grid(row=2, column=2)
        self.data.append(entry_username)

        label_password = customtkinter.CTkLabel(self, text="Password: ")
        label_password.grid(row=3, column=1)

        entry_password = customtkinter.CTkEntry(self, placeholder_text="password", show="*")
        entry_password.grid(row=3, column=2)
        self.data.append(entry_password)

        login_button = customtkinter.CTkButton(self, text="Login", command=lambda: self.log_user
            (controller, incorrect_data))
        login_button.grid(row=4, column=2)

        sign_up_button = customtkinter.CTkButton(self, text="Sign up", command=lambda: controller.show_frame(SignUp))
        sign_up_button.grid(row=5, column=2)

        incorrect_data = customtkinter.CTkLabel(self, text="INCORRECT USERNAME OR PASSWORD", text_color="red")

    def log_user(self, controller, label):
        """this function will try to log the user and redirect to the main page.
        If not possible it wil display a red label error."""

        # initiate sql data
        cwd = os.getcwd()
        print(cwd)
        sqlite_file = cwd + r"/project_files/database_project.db"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()

        # execute query
        sql = "select username, password, salt FROM users where username=?"
        cursor.execute(sql, [self.data[0].get()])

        # user verification with sql data
        database_tuple = cursor.fetchall()

        if len(database_tuple) == 0:
            label.grid(row=6, column=2)
            return None

        try:
            salt = database_tuple[0][2]
            kdf = Scrypt(
                salt=salt,
                length=32,
                n=2 ** 14,
                r=8,
                p=1,
            )

            kdf.verify(self.data[1].get().encode(), database_tuple[0][1])
        except cryptography.exceptions.InvalidKey:
            label.grid(row=6, column=2)

        else:

            # close cursor set the username value and show main page.
            cursor.close()
            set_value(self.data[0].get())
            # remove text from entries
            for item in self.data:
                item.delete(0, "end")
            # show main page
            controller.show_frame(MainPage)
