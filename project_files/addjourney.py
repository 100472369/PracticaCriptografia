import customtkinter
import os
import sqlite3
import mainpage
from settings import get_value, get_encryption_key
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


class AddJourney(customtkinter.CTkFrame):
    """This is the Add journey frame for our app."""

    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        self.attribute_dict = {"start": customtkinter.StringVar(), "finish": customtkinter.StringVar(),
                              "distance": customtkinter.StringVar(), "activity type": customtkinter.StringVar(),
                              "duration": customtkinter.StringVar(),
                              "elevation": customtkinter.StringVar(), "city": customtkinter.StringVar()}
        self.nonce = {"start": None, "finish": None, "activity type": None, "city": None}
        self.encrypted_data = {"start": None, "finish": None, "activity type": None, "city": None}
        self.incorrect_labels = []

        # instructions
        instructions_1 = customtkinter.CTkLabel(self, text="To insert type the correct data type in each entry.",
                                                font=("Arial", 18, 'bold'))
        instructions_1.grid(row=1, column=0, columnspan=7, pady=(100,2), padx=(10, 10))
        instructions_2 = customtkinter.CTkLabel(self,
                                                text="START: text, FINISH: text, "
                                                     "DISTANCE: number(kilometers), ACTIVITY TYPE: text",
                                                font=("Arial", 16))
        instructions_2.grid(row=2, column=0, columnspan=7, pady=2, padx=(10, 10))
        instructions_3 = customtkinter.CTkLabel(self,
                                                text="DURATION: number (hours), ELEVATION: number (meters), CITY: text",
                                                font=("Arial", 16))
        instructions_3.grid(row=3, column=0, columnspan=7, pady=(2, 10), padx=(10, 10))

        # this is used for deleting the entries once an operation is complete
        entry_list = []
        # used for giving values to labels
        list_values = list(self.attribute_dict.keys())

        # create labels and entries
        j = 0
        for item in list_values:
            label = customtkinter.CTkLabel(self, text=f"{item}", font=("Arial", 14, 'bold'))
            label.grid(row=4, column=j)
            entry = customtkinter.CTkEntry(self, placeholder_text="attribute",
                                           textvariable=self.attribute_dict[f"{item}"],
                                           width=144)
            entry.grid(row=5, column=j, pady=5, padx=(2,2))
            entry_list.append(entry)
            j += 1
        # extra buttons
        button = customtkinter.CTkButton(self, text="ADD JOURNEY", text_color="#3E4B3C",
                                         command=lambda: self.add_to_database(controller, entry_list),
                                         fg_color="#91D53E", hover_color="#689F33", border_color="#3E4B3C",
                                         height=30, border_width=1)
        button.grid(row=6, column=3, pady=5,padx=(10, 10))

        return_button = customtkinter.CTkButton(self, text="RETURN TO MAIN MENU", text_color="WHITE",
                                                command=lambda: self.show_main_menu(controller, entry_list),
                                                fg_color="#91D53E", hover_color="#689F33", border_color="WHITE",
                                                height=30, border_width=1)
        return_button.grid(row=7, column=3, pady=5)

        # for returning errors in insertion
        error_text = ["INCORRECT FORMAT OF DISTANCE OR DURATION OR ELEVATION",
                      "START, FINISH, TRAVEL METHOD, CITY CAN NOT BE EMPTY",
                      "DISTANCE OR DURATION CAN NOT BE NEGATIVE"]
        for item in error_text:
            label = customtkinter.CTkLabel(self, text=f"{item}", text_color="red")

            self.incorrect_labels.append(label)

    def add_to_database(self, controller, entry_list):
        """This function will insert the data into the database and return the user to the main page.
        If the data is not in the correct format, then it will display a red warning label."""

        # delete previous incorrect labels
        for item in self.incorrect_labels:
            item.grid_remove()

        cwd = os.getcwd()
        sqlite_file = cwd + r"/project_files/database_project.db"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()

        # for executing queries with foreign keys
        cursor.execute("""PRAGMA foreign_keys=ON;""")

        # create table
        sql = ("""create table if not exists bike_routes
                (
                start         BLOB not null,
                finish        BLOB not null,
                distance      REAL not null,
                activity_type BLOB not null,
                duration      REAL not null,
                elevation     REAL not null,
                city          BLOB not null,
                username      TEXT not null,
                nonce_start BLOB not null,
                nonce_finish BLOB not null,
                nonce_activity_type BLOB not null,
                nonce_city BLOB not null 
                        constraint bike_routes_users_username_fk
                            references users
                );""")
        cursor.execute(sql)
        # check parameters
        if self.check_parameters() is False:
            return None

        # encrypt the data before inserting to table
        self.encrypt_data()

        # insert into table
        sql = ("""insert into  bike_routes(start, finish, distance, activity_type, duration, elevation, 
        city, username, nonce_start, nonce_finish, nonce_activity_type, nonce_city)
            values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""")

        cursor.execute(sql, [self.encrypted_data["start"], self.encrypted_data["finish"],
                             float(self.attribute_dict["distance"].get()), self.encrypted_data["activity type"],
                             float(self.attribute_dict["duration"].get()),
                             float(self.attribute_dict["elevation"].get()),
                             self.encrypted_data["city"], get_value(), self.nonce["start"], self.nonce["finish"],
                             self.nonce["activity type"], self.nonce["city"]])

        conn.commit()
        cursor.close()
        # delete entry text
        for item in entry_list:
            item.delete(0, "end")

        #  write message in log
        messages = [f"Add journey information for user: {get_value()}",
                    "Successfully encrypted journey data.", "Algorithm used: ChaCha. Length of key: 32\n"]
        controller.write_log(messages)

        # load main page
        controller.show_frame(mainpage.MainPage)

    def check_parameters(self):
        """This function will check the insertion parameters and load the respective errors into the frame."""
        try:
            tuple_check_parameters = (self.attribute_dict["start"].get(), self.attribute_dict["finish"].get(),
                                      float(self.attribute_dict["distance"].get()),
                                      self.attribute_dict["activity type"].get(),
                                      float(self.attribute_dict["duration"].get()),
                                      float(self.attribute_dict["elevation"].get()), self.attribute_dict["city"].get(),
                                      get_value())
        except ValueError:
            self.incorrect_labels[0].grid(row=8, column=2, columnspan=3)
            return False
        for i in tuple_check_parameters:
            if not str(i).strip():
                self.incorrect_labels[1].grid(row=8, column=2, columnspan=3)
                return False
        if tuple_check_parameters[2] < 0 or tuple_check_parameters[4] < 0:
            self.incorrect_labels[2].grid(row=8, column=2, columnspan=3)
            return False
        return True

    def show_main_menu(self, controller, entry_list):
        """This function will delete the text of the entries and show the main page frame."""
        for item in entry_list:
            item.delete(0, "end")

        controller.show_frame(mainpage.MainPage)

    def encrypt_data(self):
        """This funtion will encrypt the data."""
        # get global key
        key = get_encryption_key()

        # create the 4 nonce's for each encryption
        for item in self.nonce.keys():
            self.nonce[f"{item}"] = os.urandom(12)

        # encrypt data
        chacha = ChaCha20Poly1305(key)

        for item in self.encrypted_data.keys():
            encrypted_item = chacha.encrypt(self.nonce[f"{item}"], self.attribute_dict[f"{item}"].get().encode(), None)
            self.encrypted_data[f"{item}"] = encrypted_item
