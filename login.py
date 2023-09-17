import re
import sqlite3
import os
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


class tkinterApp(customtkinter.CTk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        customtkinter.CTk.__init__(self, *args, **kwargs)

        # give title to app
        self.title("Bycycle Land")
        # change geometry
        self.geometry("800x800")

        # creating a container
        container = customtkinter.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Login, Sign_up, Main_page):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)



    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# first window frame startpage

class Login(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        # variables
        self.username = customtkinter.StringVar()
        self.password = customtkinter.StringVar()


        customtkinter.CTkFrame.__init__(self, parent)

        label = customtkinter.CTkLabel(self, text="login page")
        label.pack()

        label_username = customtkinter.CTkLabel(self, text="user name:")
        label_username.pack()

        entry_username = customtkinter.CTkEntry(self, placeholder_text="username", textvariable=self.username)
        entry_username.pack()

        label_password = customtkinter.CTkLabel(self, text="password: ")
        label_password.pack()

        entry_password = customtkinter.CTkEntry(self, placeholder_text="password", textvariable=self.password)
        entry_password.pack()

        login_button = customtkinter.CTkButton(self, text="login", command= lambda: self.log_user(controller))
        login_button.pack()

        sign_up_button = customtkinter.CTkButton(self, text="sign up", command= lambda: controller.show_frame(Sign_up))
        sign_up_button.pack()

    def log_user(self, controller):

        cwd = os.getcwd()
        sqlite_file = cwd + r"/database_project"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()


        sql = "select username, password FROM users where username=?"
        cursor.execute(sql, [self.username.get()])



        tuple_username_password = cursor.fetchall()

        if len(tuple_username_password) == 0 or tuple_username_password[0][1] != self.password.get():
            print("incorrect username or password")
        else:
            cursor.close()
            controller.show_frame(Main_page)




# second window frame page1
class Sign_up(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        #variables
        self.username = customtkinter.StringVar()
        self.password = customtkinter.StringVar()



        customtkinter.CTkFrame.__init__(self, parent)
        label = customtkinter.CTkLabel(self, text="Sign Up")
        label.pack()

        specifications_username = customtkinter.CTkLabel(self,
                                                         text="The username should be at least 6 characters long and should only contain "
                                                              "numbers, letters, hyphens and underscores.")
        specifications_username.pack()

        entry_username = customtkinter.CTkEntry(self, placeholder_text="username", textvariable=self.username)
        entry_username.pack()

        specifications_password = customtkinter.CTkLabel(self,
                                                         text="the password should be at least 8 characters long and should contain a "
                                                              "number, a letter and a special symbol ! # $ % & * + - , . : ; ? @ ~")
        specifications_password.pack()

        entry_password = customtkinter.CTkEntry(self, placeholder_text="password", textvariable=self.password)
        entry_password.pack()

        sign_up_button = customtkinter.CTkButton(self, text="Sign Up", command= lambda: self.sign_up_regex(controller))
        sign_up_button.pack()


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





# third window frame page2
class Main_page(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        label = customtkinter.CTkLabel(self, text="Page 2")
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = customtkinter.CTkButton(self, text="Page 1",
                                          command=lambda: controller.show_frame(Sign_up))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        button2 = customtkinter.CTkButton(self, text="Startpage",
                                          command=lambda: controller.show_frame(Login))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)

app = tkinterApp()
app.mainloop()
