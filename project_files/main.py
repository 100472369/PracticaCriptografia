import customtkinter
from login import Login
from sign_up import Sign_up
from main_page import Main_page
from add_journey import Add_journey
from view_journeys import View_journeys





class tkinterApp(customtkinter.CTk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        customtkinter.CTk.__init__(self, *args, **kwargs)

        # give title to app
        self.title("Bycycle Land")
        # change geometry
        self.geometry("1000x1000")


        # creating a container
        container = customtkinter.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}


        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Login, Sign_up, Main_page, Add_journey, View_journeys):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)




    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


app = tkinterApp()
app.mainloop()
