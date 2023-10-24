import customtkinter
from login import Login
from signup import SignUp
from mainpage import MainPage
from addjourney import AddJourney
from viewjourneys import ViewJourneys
import logging
import os
from settings import get_value


class Tkinterapp(customtkinter.CTk):
    """Main class for our app. Where all the different frames are created."""
    def __init__(self, *args, **kwargs):
        """Init method for class."""
        customtkinter.CTk.__init__(self, *args, **kwargs)

        # give title to app
        self.title("Bycycle Land")
        # change geometry
        self.geometry("1050x600")

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
        """Used to display the frame passed as parameter."""
        frame = self.frames[cont]
        frame.tkraise()

    def write_log(self, messages: list):
        """This function will write log details into a file when encryption, verification or decryption occurs."""
        cwd = os.getcwd()
        # create folder if not exists
        directory = cwd + "/log_files"
        if not os.path.exists(directory):
            os.makedirs(directory)

        username = get_value()
        file_name = cwd + f"/log_files/{username}.log"

        logging.basicConfig(filename=f"{file_name}", level=logging.INFO)
        logging.info(f"{messages[0]}")
        logging.info(f"{messages[1]}")
        logging.info(f"{messages[2]}")


app = Tkinterapp()
app.mainloop()
