import customtkinter
from add_journey import Add_journey
from view_journeys import View_journeys


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

