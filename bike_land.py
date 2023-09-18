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
        self.geometry("1000x1000")

        # creating a container
        container = customtkinter.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Login, Sign_up, Main_page, Add_journey, View_journeys):
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


        entry_password = customtkinter.CTkEntry(self, placeholder_text="password", textvariable=self.password)
        entry_password.grid(row=3, column=2)


        login_button = customtkinter.CTkButton(self, text="login", command= lambda: self.log_user(controller))
        login_button.grid(row=4, column=2)


        sign_up_button = customtkinter.CTkButton(self, text="sign up", command= lambda: controller.show_frame(Sign_up))
        sign_up_button.grid(row=5, column=2)


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





# third window frame page2
class Main_page(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)

        welcome_message = customtkinter.CTkLabel(self, text="Welcome to bike land")
        welcome_message.grid()


        options_message = (customtkinter.CTkLabel(self, text="You have two options: "
                                                              "\n1) add a journey \n2) view added journeys"))
        options_message.grid()

        add_journey = customtkinter.CTkButton(self, text="Add a journey",
         command=lambda: controller.show_frame(Add_journey))
        add_journey.grid()

        view_journeys = customtkinter.CTkButton(self, text="View journeys",
                                command=lambda: controller.show_frame(View_journeys))
        view_journeys.grid()

class Add_journey(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        self.atribute_dict = {"start": customtkinter.StringVar(), "finish": customtkinter.StringVar(),
                              "distance": customtkinter.StringVar(), "travel method": customtkinter.StringVar(),
                              "duration":customtkinter.StringVar(),
                              "elevation": customtkinter.StringVar(), "city": customtkinter.StringVar()}



        list_values = list(self.atribute_dict.keys())

        j = 0
        for item in list_values:
            label = customtkinter.CTkLabel(self, text=f"{item}")
            label.grid(row=1, column=j)
            entry = customtkinter.CTkEntry(self, placeholder_text="atribute", textvariable=self.atribute_dict[f"{item}"])
            entry.grid(row=2, column=j)
            j += 1

        button = customtkinter.CTkButton(self, text="ADD JOURNEY", command=lambda: self.add_to_database())
        button.grid(row=4, column=3)

    def add_to_database(self):
        cwd = os.getcwd()
        sqlite_file = cwd + r"/database_project"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()


        # create table
        sql = ("""create table if not exists bike_routes
        (start         TEXT, 
        finish        TEXT, 
        distance      REAL, 
        travel_method TEXT, 
        elevation     REAL, 
        city          TEXT, 
        username      TEXT 
        constraint "bike routes___fk" references users);""")
        cursor.execute(sql)

        # insert into table
        sql = ("""insert into  bike_routes(start, finish, distance, travel_method, duration, elevation, city)
            values (?, ?, ?, ?, ?, ?, ?)""")

        tuple_insert = (self.atribute_dict["start"].get(), self.atribute_dict["finish"].get(),
                             int(self.atribute_dict["distance"].get()), self.atribute_dict["travel method"].get(),
                            int(self.atribute_dict["duration"].get()),
                             int(self.atribute_dict["elevation"].get()), self.atribute_dict["city"].get())
        cursor.execute(sql, tuple_insert)


        conn.commit()
        cursor.close()

class View_journeys(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        rows = None
        columns = None

        cwd = os.getcwd()
        sqlite_file = cwd + r"/database_project"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()

        sql = ("select start, finish, distance,travel_method, duration, elevation, city from bike_routes;")
        cursor.execute(sql)
        query = cursor.fetchall()


        atribute_names = ["start", "finish", "distance", "travel method", "duration", "elevation", "city"]


        # cree estos entries para que se aline la info no se como todo
        for i in range(7):
            entry = customtkinter.CTkEntry(self, placeholder_text=f"{atribute_names[i]}")
            entry.grid(row =1, column=i)



        i = 2
        for item in query:

            for j in range(len(item)):
                label = customtkinter.CTkLabel(self, text=f"{item[j]}")
                label.grid(row=i, column=j)
            i += 1









app = tkinterApp()
app.mainloop()
