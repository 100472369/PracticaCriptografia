import re
import sqlite3
import os
import tkinter

import customtkinter



# este es el antiguo login se usara despues por eso se queda
# print("welcome to BikeLand.\n")
# print("You will be asked to enter a username. The restrctions of a username are the following:\n")
# print("The username should be at least 6 characters long and should only contain numbers, letters, \n")
# print("hyphens and underscores.\n")
#
# username = input("please input your username: ")
# print("You will be asked to enter a username. The restrctions of a password are the following:\n")
# print("the password should be at least 8 characters long and should contain a number, a letter\n")
# print("and a special symbol ! # $ % & * + - , . : ; ? @ ~\n")
# password = input("please input your password: ")
#
# regex_username = "^[a-zA-z0-9]{6,}$"
# regex_password = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!#$%&*+_,.:;?@~]).{8,}$"
#
# if re.fullmatch(regex_username, username) is None or re.fullmatch(regex_password, password) is None:
#     raise ValueError("The password or username you entered does not conform to the rules established")
#
# # insert the username and password int sql table
# cwd = os.getcwd()
# sqlite_file = cwd + r"/database_project"
# conn = sqlite3.connect(sqlite_file)
# cursor = conn.cursor()
#
# sql = ("create table if not exists users "
#        "(username TEXT not null constraint users_pk primary key, password TEXT not null);")
# cursor.execute(sql)
#
#
#
# sql = "INSERT INTO users (username, password) VALUES " + f"(\"{username}\", \"{password}\");"
# cursor.execute(sql)
#
# conn.commit()
# cursor.close()





class App:
    def __init__(self, root = customtkinter.CTk()):

        self.root = root
        self.root.geometry("800x600")
        self.root.title("Bycyle land")
        self.username = customtkinter.StringVar()
        self.pasword = customtkinter.StringVar()



    def manager(self):
        """This function will manage the aplication by running the respective funtions"""

        self.login()

        self.root.mainloop()

    def login(self):
        """This function will load the login GUI"""

        frame = customtkinter.CTkFrame(self.root, fg_color="blue")
        frame.pack()
        label = customtkinter.CTkLabel(frame, text="login page")
        label.pack()

        label_username = customtkinter.CTkLabel(frame, text="user name:")
        label_username.pack()

        entry_username = customtkinter.CTkEntry(frame, placeholder_text="username",
                                                     textvariable=self.username)
        entry_username.pack()

        label_password = customtkinter.CTkLabel(frame, text="password: ")
        label_password.pack()

        entry_password = customtkinter.CTkEntry(frame, placeholder_text="password", textvariable=self.pasword)
        entry_password.pack()

        login_button = customtkinter.CTkButton(frame, text="login", command=lambda: self.login_user())
        login_button.pack()


        sign_up_button = customtkinter.CTkButton(frame, text="sign up", command=lambda: self.sign_up())
        sign_up_button.pack()

    def login_user(self):
        self.logged_in = True

    def sign_up(self):
        """this function will load the register page"""
        frame = customtkinter.CTkFrame(self.root, fg_color="red")
        frame.pack()

        specifications_username = customtkinter.CTkLabel(frame, text="The username should be at least 6 characters long and should only contain "
                                                          "numbers, letters, hyphens and underscores.")
        specifications_username.pack()

        entry_username = customtkinter.CTkEntry(frame, placeholder_text="username")
        entry_username.pack()

        specifications_password = customtkinter.CTkLabel(frame, text="the password should be at least 8 characters long and should contain a "
                                                              "number, a letter and a special symbol ! # $ % & * + - , . : ; ? @ ~")
        specifications_password.pack()

        entry_password = customtkinter.CTkEntry(frame, placeholder_text="password")
        entry_password.pack()

app = App()
app.manager()





