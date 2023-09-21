import re
import sqlite3
import os
import customtkinter




# second window frame page1
class Sign_up(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        #variables
        self.username = customtkinter.StringVar()
        self.password = customtkinter.StringVar()


        customtkinter.CTkFrame.__init__(self, parent)




        label = customtkinter.CTkLabel(self, text="Sign Up")
        label.grid(row=1, column=1)

        specifications_username = customtkinter.CTkLabel(self,
                                                         text="The username should be at least 6 characters long and should only contain "
                                                              "numbers, letters, hyphens and underscores.")
        specifications_username.grid(row=2, column=1)

        entry_username = customtkinter.CTkEntry(self, placeholder_text="username", textvariable=self.username)
        entry_username.grid(row=3, column=1)

        specifications_password = customtkinter.CTkLabel(self,
                                                         text="          The password should be at least 8 characters "
                                                              "long and should contain a "
                                                              "number, a letter and a special symbol "
                                                              "! # $ % & * + - , . : ; ? @ ~")
        specifications_password.grid(row=4, column=1)


        entry_password = customtkinter.CTkEntry(self, placeholder_text="password", textvariable=self.password)
        entry_password.grid(row=5, column=1)

        sign_up_button = customtkinter.CTkButton(self, text="Sign Up", command= lambda: self.sign_up_regex(controller))
        sign_up_button.grid(row=6, column=1)


    def sign_up_regex(self, controller):
        regex_username = "^[a-zA-z0-9]{6,}$"
        regex_password = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!#$%&*+_,.:;?@~]).{8,}$"

        if (re.fullmatch(regex_username, self.username.get()) is None or
                re.fullmatch(regex_password, self.password.get()) is None):
            print("wrong format")
        else:
            self.register_user(controller)
    def register_user(self, controller):
        cwd = os.getcwd()
        sqlite_file = cwd + r"/database_project"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()

        sql = ("create table if not exists users "
               "(username TEXT not null constraint users_pk primary key, password TEXT not null);")
        cursor.execute(sql)

        # first check if username exists

        sql = "select username from users where username=?"
        cursor.execute(sql, [self.username.get()])

        username = cursor.fetchall()
        if len(username) != 0:
            print("username already exists")
        else:
            sql = ("INSERT INTO users (username, password) VALUES " +
                   f"(\"{self.username.get()}\", \"{self.password.get()}\");")
            cursor.execute(sql)

            conn.commit()
            cursor.close()

            controller.show_frame(Main_page)