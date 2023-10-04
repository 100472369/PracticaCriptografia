import customtkinter
import os
import sqlite3
import main_page
from settings import get_value

class View_journeys(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        button = customtkinter.CTkButton(self, text="SHOW JOURNEYS", command=lambda:self.run_query())
        button.grid(row=1, column=3, pady=5)

        return_menu = customtkinter.CTkButton(self, text="RETURN TO MAIN MENU",
                                              command=lambda: controller.show_frame(main_page.Main_page))
        return_menu.grid(row=2, column=3, pady=5)

    def run_query(self):
        rows = None
        columns = None


        cwd = os.getcwd()
        sqlite_file = cwd + r"/database_project"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()
        # for executing queries with foreign keys
        cursor.execute("""PRAGMA foreign_keys=ON;""")

        sql = ("select start, finish, distance,travel_method, "
               f"duration, elevation, city from bike_routes where username=?;")
        cursor.execute(sql, [get_value()])
        query = cursor.fetchall()


        attribute_names = ["start", "finish", "distance(kilometers)", "travel method", "duration(hours)", "elevation(meters)", "city"]
        string_var_items = []
        for item in attribute_names:
            string_var_items.append(customtkinter.StringVar(self, f"{item}"))



        # cree estos entries para que se aline la info no se como todo
        for i in range(len(attribute_names)):
            entry = customtkinter.CTkEntry(self, textvariable=string_var_items[i], state="readonly")
            entry.grid(row =3, column=i)



        i = 4
        for item in query:
            for j in range(len(item)):
                label = customtkinter.CTkLabel(self, text=f"{item[j]}")
                label.grid(row=i, column=j)
            i += 1
