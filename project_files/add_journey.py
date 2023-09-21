import customtkinter
import os
import sqlite3


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