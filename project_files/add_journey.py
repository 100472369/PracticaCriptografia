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



        list_values = list(self.atribute_dict.keys())

        j = 0
        for item in list_values:
            label = customtkinter.CTkLabel(self, text=f"{item}")
            label.grid(row=1, column=j)
            entry = customtkinter.CTkEntry(self, placeholder_text="atribute", textvariable=self.atribute_dict[f"{item}"])
            entry.grid(row=2, column=j)
            j += 1

        button = customtkinter.CTkButton(self, text="ADD JOURNEY",
                                         command=lambda: self.add_to_database(controller, incorrect_query))
        button.grid(row=4, column=3)

        return_button = customtkinter.CTkButton(self, text="RETURN TO MAIN MENU",
                                                command=lambda:controller.show_frame(main_page.Main_page))
        return_button.grid(row=5, column=3)

        incorrect_query = customtkinter.CTkLabel(self, text="Wrong format", text_color="red")




    def add_to_database(self, controller, label):

        cwd = os.getcwd()
        sqlite_file = cwd + r"/database_project"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()

        # for executing queries with foreign keys
        cursor.execute("""PRAGMA foreign_keys=ON;""")



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

        try:
            tuple_insert = (self.atribute_dict["start"].get(), self.atribute_dict["finish"].get(),
                        float(self.atribute_dict["distance"].get()), self.atribute_dict["travel method"].get(),
                        float(self.atribute_dict["duration"].get()),
                        float(self.atribute_dict["elevation"].get()), self.atribute_dict["city"].get(),
                        get_value())
        except ValueError:
            label.grid(row=6, column=3)
            return None

        for i in tuple_insert:
            if not str(i).strip():
                label.grid(row=6, column=3)
                return None

        # insert into table
        sql = ("""insert into  bike_routes(start, finish, distance, travel_method, duration, elevation, city, username)
            values (?, ?, ?, ?, ?, ?, ?, ?)""")


        cursor.execute(sql, tuple_insert)


        conn.commit()
        cursor.close()

        controller.show_frame(main_page.Main_page)
