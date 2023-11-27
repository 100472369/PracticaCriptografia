import customtkinter
# import frames
from addjourney import AddJourney
from viewjourneys import ViewJourneys
import login
# functions used
from settings import get_value


class MainPage(customtkinter.CTkFrame):
    """This is the Main page frame for our app."""

    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        # used to center page
        self.grid_columnconfigure(0, weight=1)

        # labels and buttons of main menu
        welcome_message = customtkinter.CTkLabel(self, text="Welcome to Bicycle Land", font=("Impact", 25))
        welcome_message.grid(pady=(120, 6))

        options_message = (customtkinter.CTkLabel(self, text="You have two options: "
                                                             "\n1) Add a journey \n2) View added journeys",
                                                        font=("Trebuchet MS", 18)))
        options_message.grid(pady=5)

        add_journey = customtkinter.CTkButton(self, text="Add a journey", text_color="#3E4B3C", font=("Arial", 16),
                                              command=lambda: controller.show_frame(AddJourney),
                                              fg_color="#91D53E", hover_color="#689F33", border_color="#3E4B3C",
                                              height=30, border_width=1, width=200)
        add_journey.grid(pady=5)

        view_journeys = customtkinter.CTkButton(self, text="View journeys", text_color="#3E4B3C", font=("Arial", 16),
                                                command=lambda: controller.show_frame(ViewJourneys),
                                                fg_color="#91D53E", hover_color="#689F33", border_color="#3E4B3C",
                                                height=30, border_width=1, width=200)
        view_journeys.grid(pady=5)

        confirmation = customtkinter.CTkLabel(self, text="ARE YOU SURE?", text_color="RED")
        yes_button = customtkinter.CTkButton(self, text="YES", text_color="RED",
                                             command=lambda: self.delete_user(controller, yes_button,
                                                                              no_button, confirmation),
                                             fg_color="WHITE", hover_color="#FDFACB", border_color="RED",
                                             height=30, border_width=1)

        no_button = customtkinter.CTkButton(self, text="NO", text_color="GREEN", command=lambda:
            self.remove_confirmation(confirmation, yes_button, no_button),
                                            fg_color="WHITE", hover_color="#FDFACB", border_color="GREEN",
                                            height=30, border_width=1)

        delete_account = customtkinter.CTkButton(self, text="DELETE ACCOUNT", fg_color="red", font=("Arial", 13),
                                                 command=lambda: self.are_you_sure(yes_button, no_button, confirmation),
                                                 hover_color="#E65C5F", border_color="#FFFFFF",
                                                 height=30, border_width=1, width=200)
        delete_account.grid(pady=5)

    def are_you_sure(self, yes, no, confirmation):
        """This function will load the yes no confirmation buttons when delete account is pressed."""
        confirmation.grid()
        yes.grid(pady=2)
        no.grid(pady=2)

    def remove_confirmation(self, confirmation, yes, no):
        """This function will remove the confirmation buttons when 'no' is pressed."""
        confirmation.grid_remove()
        yes.grid_remove()
        no.grid_remove()

    def delete_user(self, controller, yes, no, confirmation):
        """This function will delete the user signature and their trips from the database.
        It will then return the user to the login frame."""
        sqlite = controller.initialize_sql()
        conn = sqlite[0]
        cursor = sqlite[1]

        # for executing queries with foreign keys
        cursor.execute("""PRAGMA foreign_keys=ON;""")
        # removal of user, signature, trips

        sql = """delete from users where username =?;"""
        cursor.execute(sql, [get_value()])
        conn.commit()
        cursor.close()
        # remove confirmation buttons
        self.remove_confirmation(confirmation, yes, no)
        # load login frame
        controller.show_frame(login.Login)
