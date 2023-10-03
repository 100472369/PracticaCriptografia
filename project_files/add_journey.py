import customtkinter
import os
import sqlite3
import main_page
from settings import get_value

class Add_journey(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        self.atribute_dict = {"start": customtkinter.StringVar(), "finish": customtkinter.StringVar(),
                              "distance": customtkinter.StringVar(), "travel method": customtkinter.StringVar(),
                              "duration":customtkinter.StringVar(),
                              "elevation": customtkinter.StringVar(), "city": customtkinter.StringVar()}

        # instructions
        instructions_1 = customtkinter.CTkLabel(self, text="To insert type the correct data type in each entry.")
        instructions_1.grid(row=1, column=2, columnspan=3)
        instructions_2 = customtkinter.CTkLabel(self, text="START: text, FINISH: text, DISTANCE: number(kilometers), TRAVEL METHOD: text")
        instructions_2.grid(row=2, column=2, columnspan=3)
        instructions_3 = customtkinter.CTkLabel(self, text="DURATION: number (hours), ELEVATION: number (meters), CITY: TEXT")
        instructions_3.grid(row=3, column=2, columnspan=3)



        # this is used for deleteing the entries once an operation is complete
        entry_list = []
        # used for giving values to labels
        list_values = list(self.atribute_dict.keys())

        # create labels and entries
        j = 0
        for item in list_values:
            label = customtkinter.CTkLabel(self, text=f"{item}")
            label.grid(row=4, column=j)
            entry = customtkinter.CTkEntry(self, placeholder_text="atribute", textvariable=self.atribute_dict[f"{item}"])
            entry.grid(row=5, column=j)
            entry_list.append(entry)
            j += 1
        # extra buttons
        button = customtkinter.CTkButton(self, text="ADD JOURNEY",
                                         command=lambda: self.add_to_database(controller, incorrect_query, entry_list))
        button.grid(row=6, column=3)

        return_button = customtkinter.CTkButton(self, text="RETURN TO MAIN MENU",
                                                command=lambda: self.show_main_menu(controller, entry_list))
        return_button.grid(row=7, column=3)

        incorrect_query = customtkinter.CTkLabel(self, text="Wrong format", text_color="red")





    def add_to_database(self, controller, label, entry_list):
        """This function will insert the data into the database and return the user to the main page.
        If it gets and error while inserting then it will display a red warning label."""
        cwd = os.getcwd()
        sqlite_file = cwd + r"/database_project"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()

        # for executing queries with foreign keys
        cursor.execute("""PRAGMA foreign_keys=ON;""")


        # create table
        sql = ("""create table if not exists bike_routes
                (
                start         TEXT not null,
                finish        TEXT not null,
                distance      REAL not null,
                travel_method TEXT not null,
                duration      REAL not null,
                elevation     REAL not null,
                city          TEXT not null,
                username      TEXT 
                        constraint bike_routes_users_username_fk
                            references users
                );""")
        cursor.execute(sql)

        # insert into
        try:
            tuple_insert = (self.atribute_dict["start"].get(), self.atribute_dict["finish"].get(),
                        float(self.atribute_dict["distance"].get()), self.atribute_dict["travel method"].get(),
                        float(self.atribute_dict["duration"].get()),
                        float(self.atribute_dict["elevation"].get()), self.atribute_dict["city"].get(),
                        get_value())
        except ValueError:
            label.grid(row=8, column=3)
            return None

        for i in tuple_insert:

            if not str(i).strip():
                label.grid(row=8, column=3)
                return None

        # insert into table
        sql = ("""insert into  bike_routes(start, finish, distance, travel_method, duration, elevation, city, username)
            values (?, ?, ?, ?, ?, ?, ?, ?)""")


        cursor.execute(sql, tuple_insert)


        conn.commit()
        cursor.close()

        for item in entry_list:
            item.delete(0, "end")


        controller.show_frame(main_page.Main_page)


    def show_main_menu(self, controller, entry_list):
        for item in entry_list:
            item.delete(0, "end")

        controller.show_frame(main_page.Main_page)
