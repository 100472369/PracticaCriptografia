import customtkinter
from add_journey import Add_journey
from view_journeys import View_journeys
from settings import get_value
import os
import sqlite3
import login


class Main_page(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        # used to center page
        self.grid_columnconfigure(0, weight=1)

        # labels and buttons of main menu
        welcome_message = customtkinter.CTkLabel(self, text="Welcome to bike land")
        welcome_message.grid()


        options_message = (customtkinter.CTkLabel(self, text="You have two options: "
                                                              "\n1) add a journey \n2) view added journeys"))
        options_message.grid()

        add_journey = customtkinter.CTkButton(self, text="Add a journey",
         command=lambda: controller.show_frame(Add_journey))
        add_journey.grid(pady=5)

        view_journeys = customtkinter.CTkButton(self, text="View journeys",
                                command=lambda: controller.show_frame(View_journeys))
        view_journeys.grid(pady=5)

        confirmation = customtkinter.CTkLabel(self, text="ARE YOU SURE?", text_color="RED")
        yes_button = customtkinter.CTkButton(self, text="YES", command=lambda: self.delete_user(controller))
        no_button = customtkinter.CTkButton(self, text="NO", command= lambda:
        self.remove_confirmation(confirmation, yes_button, no_button))

        delete_account = customtkinter.CTkButton(self, text="DELETE ACCOUNT", fg_color="red",
                                                 command= lambda: self.are_you_sure(yes_button, no_button, confirmation))
        delete_account.grid(pady=5)


    def are_you_sure(self, yes, no, confirmation):
        confirmation.grid()
        yes.grid()
        no.grid()

    def remove_confirmation(self, confirmation, yes, no):
        confirmation.grid_remove()
        yes.grid_remove()
        no.grid_remove()

    def delete_user(self, controller):
        cwd = os.getcwd()
        sqlite_file = cwd + r"/database_project"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()

        # for executing queries with foreign keys
        cursor.execute("""PRAGMA foreign_keys=ON;""")


        sql = """delete from bike_routes where username = ?"""
        cursor.execute(sql, [get_value()])

        sql = """delete from users where username =?;"""
        cursor.execute(sql, [get_value()])


        conn.commit()
        cursor.close()

        controller.show_frame(login.Login)



