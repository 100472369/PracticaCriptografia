import re
import sqlite3
import os
import tkinter
from tkinter import *
from tkinter.ttk import *



# este es el antiguo login se usara despues por eso se queda
"""print("welcome to BikeLand.\n")
print("You will be asked to enter a username. The restrctions of a username are the following:\n")
print("The username should be at least 6 characters long and should only contain numbers, letters, \n")
print("hyphens and underscores.\n")

username = input("please input your username: ")
print("You will be asked to enter a username. The restrctions of a password are the following:\n")
print("the password should be at least 8 characters long and should contain a number, a letter\n")
print("and a special symbol ! # $ % & * + - , . : ; ? @ ~\n")
password = input("please input your password: ")

regex_username = "^[a-zA-z0-9]{6,}$"
regex_password = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!#$%&*+_,.:;?@~]).{8,}$"

if re.fullmatch(regex_username, username) is None or re.fullmatch(regex_password, password) is None:
    raise ValueError("The password or username you entered does not conform to the rules established")

# insert the username and password int sql table
cwd = os.getcwd()
sqlite_file = cwd + r"/database_project"
conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor()

sql = ("create table if not exists users "
       "(username TEXT not null constraint users_pk primary key, password TEXT not null);")
cursor.execute(sql)



sql = "INSERT INTO users (username, password) VALUES " + f"(\"{username}\", \"{password}\");"
cursor.execute(sql)

conn.commit()
cursor.close()"""

class App:

    def __init__(self, root):
        self.root = root
        self.username = None
        self.pasword = None

    def login_page(self):
        self.root.geometry("800x800")
        self.root.title("bycle map")

        root_title = tkinter.Label(self.root, text="login page", font="arial")
        root_title.pack()


        frame = tkinter.Frame(self.root, borderwidth=2)
        frame.pack()

        username_label = tkinter.Label(frame, text='Username', font=('calibre', 10, 'bold'))
        username_label.pack()
        entry_username = tkinter.Entry(frame)
        entry_username.pack()

        password_label = tkinter.Label(frame, text='Username', font=('calibre', 10, 'bold'))
        password_label.pack()
        entry_password = tkinter.Entry(frame, show="*")
        entry_password.pack()

        login_button = tkinter.Button(frame, text="login")
        login_button.pack()

        sing_up_button = tkinter.Button(frame, text="sign up")
        sing_up_button.pack()


root = tkinter.Tk()
app = App(root)
app.login_page()
root.mainloop()

