import sqlite3
import os
import customtkinter
from sign_up import Sign_up
from main_page import Main_page
from settings import set_value


class Login(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        # variables
        self.username = customtkinter.StringVar()
        self.password = customtkinter.StringVar()
        self.incorrect_data = False



        customtkinter.CTkFrame.__init__(self, parent)
        # this is used to center all the elemetns
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(4, weight=2)


        label = customtkinter.CTkLabel(self, text="login page")
        label.grid(row=1, column=2)


        label_username = customtkinter.CTkLabel(self, text="user name:")
        label_username.grid(row=2, column=1)


        entry_username = customtkinter.CTkEntry(self, placeholder_text="username", textvariable=self.username)
        entry_username.grid(row=2, column=2)


        label_password = customtkinter.CTkLabel(self, text="password: ")
        label_password.grid(row=3, column=1)


        entry_password = customtkinter.CTkEntry(self, placeholder_text="password", textvariable=self.password, show="*")
        entry_password.grid(row=3, column=2)


        login_button = customtkinter.CTkButton(self, text="login", command= lambda: self.log_user(controller, incorrect_data))
        login_button.grid(row=4, column=2)


        sign_up_button = customtkinter.CTkButton(self, text="sign up", command= lambda: controller.show_frame(Sign_up))
        sign_up_button.grid(row=5, column=2)


        incorrect_data = customtkinter.CTkLabel(self, text="INCORRECT USERNAME OR PASSWORD", text_color="red")





    def log_user(self, controller, label):

        cwd = os.getcwd()
        sqlite_file = cwd + r"/database_project"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()


        sql = "select username, password FROM users where username=?"
        cursor.execute(sql, [self.username.get()])



        tuple_username_password = cursor.fetchall()

        if len(tuple_username_password) == 0 or tuple_username_password[0][1] != self.password.get():
            label.grid(row=6, column=2)

        else:
            cursor.close()
            set_value(self.username.get())

            controller.show_frame(Main_page)

