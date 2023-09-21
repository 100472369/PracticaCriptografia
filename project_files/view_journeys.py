import customtkinter
import os
import sqlite3


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


        attribute_names = ["start", "finish", "distance", "travel method", "duration", "elevation", "city"]


        # cree estos entries para que se aline la info no se como todo
        for i in range(len(attribute_names)):
            entry = customtkinter.CTkEntry(self, placeholder_text=f"{attribute_names[i]}", state="disabled")
            entry.grid(row =1, column=i)



        i = 2
        for item in query:
            for j in range(len(item)):
                label = customtkinter.CTkLabel(self, text=f"{item[j]}")
                label.grid(row=i, column=j)
            i += 1