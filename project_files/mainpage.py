import customtkinter
from addjourney import AddJourney
from viewjourneys import ViewJourneys
from settings import get_value
import os
import sqlite3
import login


class MainPage(customtkinter.CTkFrame):
    """This is the Main page frame for our app."""

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
                                              command=lambda: controller.show_frame(AddJourney))
        add_journey.grid(pady=5)

        view_journeys = customtkinter.CTkButton(self, text="View journeys",
                                                command=lambda: controller.show_frame(ViewJourneys))
        view_journeys.grid(pady=5)

        confirmation = customtkinter.CTkLabel(self, text="ARE YOU SURE?", text_color="RED")
        yes_button = customtkinter.CTkButton(self, text="YES",
                                             command=lambda: self.delete_user(controller, yes_button,
                                                                              no_button, confirmation))
        no_button = customtkinter.CTkButton(self, text="NO", command=lambda:
            self.remove_confirmation(confirmation, yes_button, no_button))

        delete_account = customtkinter.CTkButton(self, text="DELETE ACCOUNT", fg_color="red",
                                                 command=lambda: self.are_you_sure(yes_button, no_button, confirmation))
        delete_account.grid(pady=5)

    def are_you_sure(self, yes, no, confirmation):
        """This function will load the yes no confirmation buttons when delete account is pressed."""
        confirmation.grid()
        yes.grid()
        no.grid()

    def remove_confirmation(self, confirmation, yes, no):
        """This function will remove the confirmation buttons when 'no' is pressed."""
        confirmation.grid_remove()
        yes.grid_remove()
        no.grid_remove()

    def delete_user(self, controller, yes, no, confirmation):
        """This function will delete aswell as their trips from the database.
        It will return the user to the login frame."""
        cwd = os.getcwd()
        sqlite_file = cwd + r"/project_files/database_project.db"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()

        # for executing queries with foreign keys
        cursor.execute("""PRAGMA foreign_keys=ON;""")
        # removable of data and user
        sql = """delete from bike_routes where username = ?"""
        cursor.execute(sql, [get_value()])

        sql = """delete from users where username =?;"""
        cursor.execute(sql, [get_value()])
        conn.commit()
        cursor.close()
        # remove confirmation buttons
        self.remove_confirmation(confirmation, yes, no)
        # load login frame
        controller.show_frame(login.Login)
