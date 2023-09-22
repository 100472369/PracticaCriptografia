import customtkinter
import os
import sqlite3
import main_page
from settings import get_value

class View_journeys(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        button = customtkinter.CTkButton(self, text="RUN QUERIES", command=lambda:self.run_query(controller))
        button.grid(row=1, column=3)

        return_menu = customtkinter.CTkButton(self, text="RETURN TO MAIN MENU",
                                              command=lambda: controller.show_frame(main_page.Main_page))
        return_menu.grid(row=2, column=3)


    def run_query(self, controller):
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


        attribute_names = ["start", "finish", "distance", "travel method", "duration", "elevation", "city"]


        # cree estos entries para que se aline la info no se como todo
        for i in range(len(attribute_names)):
            entry = customtkinter.CTkEntry(self, placeholder_text=f"{attribute_names[i]}", state="disabled")
            entry.grid(row =3, column=i)



        i = 4
        for item in query:
            for j in range(len(item)):
                label = customtkinter.CTkLabel(self, text=f"{item[j]}")
                label.grid(row=i, column=j)
            i += 1
