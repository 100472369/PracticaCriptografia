import re
import sqlite3
import os
import customtkinter
from main_page import Main_page
from settings import set_value



class Sign_up(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        #variables
        self.data = []
        self.incorrect_labels = []


        customtkinter.CTkFrame.__init__(self, parent)



        # labels, entries and buttons
        label = customtkinter.CTkLabel(self, text="Sign Up")
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
        self.data.append(entry_username)

        email = customtkinter.CTkLabel(self, text="email:")
        email.grid(row=4, column=3)
        email_entry=customtkinter.CTkEntry(self, placeholder_text="email")
        email_entry.grid(row=4, column=5)
        self.data.append(email_entry)

        phone = customtkinter.CTkLabel(self, text="phone number:")
        phone.grid(row=5, column=3)
        phone_entry = customtkinter.CTkEntry(self, placeholder_text="phone")
        phone_entry.grid(row=5, column=5)
        self.data.append(phone_entry)


        specifications_password = customtkinter.CTkLabel(self,
                                                         text="                 "
                                                              "The password should be at least 8 characters "
                                                              "long and should contain: a "
                                                              "number, a lowercase letter, "
                                                              "an upercase letter and a special symbol "
                                                              "! # $ % & * + - , . : ; ? @ ~")
        specifications_password.grid(row=6, column=1, columnspan=7)

        password = customtkinter.CTkLabel(self, text="password:")
        password.grid(row=7, column=3)
        entry_password = customtkinter.CTkEntry(self, placeholder_text="password", show="*")
        entry_password.grid(row=7, column=5)
        self.data.append(entry_password)


        repeat_password = customtkinter.CTkLabel(self, text="repeat password:")
        repeat_password.grid(row=8, column=3)
        repeat_password_entry = customtkinter.CTkEntry(self, placeholder_text="password", show="*")
        repeat_password_entry.grid(row=8, column=5)
        self.data.append(repeat_password_entry)

        # format errors
        text_display = ["WRONG FORMAT USERNAME", "WRONG FORMAT EMAIL", "WRONG FORMAT PHONE", "WRONG FORMAT PASSWORD",
                        "PASSWORDS DO NOT MATCH", "USERNAME ALREADY EXISTS"]
        for item in text_display:
            format_label = customtkinter.CTkLabel(self, text=f"{item}", text_color="red")
            self.incorrect_labels.append(format_label)


        sign_up_button = customtkinter.CTkButton(self, text="Sign Up",
                                                 command= lambda: self.check_parameters(controller,
                                                                                        self.incorrect_labels))
        sign_up_button.grid(row=9, column=4)





    def check_parameters(self, controller, incorrect_labels):
        """This functions will check the parameters established.
        If iot does it will call register_user, if not it will display a red warning label."""
        regex_username = "^[a-zA-z0-9]{6,}$"
        regex_password = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!#$%&*+_,.:;?@~]).{8,}$"
        regex_email = "^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$"
        regex_phone = "^[0-9]{9}$"

        for item in self.incorrect_labels:
            item.grid_remove()

        if re.fullmatch(regex_username, self.data[0].get()) is None:
            incorrect_labels[0].grid(row=10, column=4)

        elif re.fullmatch(regex_email, self.data[1].get()) is None:
            incorrect_labels[1].grid(row=10, column=4)

        elif re.fullmatch(regex_phone, self.data[2].get()) is None:
            incorrect_labels[2].grid(row=10, column=4)

        elif re.fullmatch(regex_password, self.data[3].get()) is None:
            incorrect_labels[3].grid(row=10, column=4)
        elif self.data[3].get() != self.data[4].get():
            incorrect_labels[4].grid(row=10, column=4)
        else:

            self.register_user(controller, incorrect_labels)
    def register_user(self, controller, incorrect_labels):
        """This function will register the user.
        If the username exists it will display a red warining label."""
        # sql initialize
        cwd = os.getcwd()
        sqlite_file = cwd + r"/database_project"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()
        # create table
        sql = ("create table if not exists users "
               "(username TEXT not null constraint users_pk primary key, password TEXT not null,"
               "email TEXT not null, phone_number TEXT not null );")
        cursor.execute(sql)

        # first check if username exists

        sql = "select username from users where username=?"
        cursor.execute(sql, [self.data[0].get()])

        username = cursor.fetchall()
        if len(username) != 0:
            for item in self.incorrect_labels:
                item.grid_remove()
            incorrect_labels[5].grid(row=10, column=4)


        else:
            # insert into table and log user
            sql = """INSERT INTO users (username, email, phone_number, password) VALUES (?, ?, ?, ?)"""

            cursor.execute(sql,
                           [self.data[0].get(), self.data[1].get(),
                            self.data[2].get(), self.data[3].get()])

            conn.commit()
            cursor.close()

            set_value(self.data[0].get())

            # remove text from entries
            for item in self.data:
                item.delete(0, "end")


            controller.show_frame(Main_page)
