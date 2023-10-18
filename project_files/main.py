import customtkinter
from login import Login
from signup import SignUp
from mainpage import MainPage
from addjourney import AddJourney
from viewjourneys import ViewJourneys


class Tkinterapp(customtkinter.CTk):
    """Main class for our app. Where all the different frames are created."""
    def __init__(self, *args, **kwargs):
        """Init method for class."""
        customtkinter.CTk.__init__(self, *args, **kwargs)

        # give title to app
        self.title("Bycycle Land")
        # change geometry
        self.geometry("1000x800")

        # creating a container
        container = customtkinter.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Login, SignUp, MainPage, AddJourney, ViewJourneys):
            frame = F(container, self)

            # initializing frame of that object from
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, cont):
        """Used to display the frame passed as parameter"""
        frame = self.frames[cont]
        frame.tkraise()


app = Tkinterapp()
app.mainloop()
