import customtkinter
import os
import sqlite3
import mainpage
from settings import get_value, get_encryption_key
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


class ViewJourneys(customtkinter.CTkFrame):
    """The View journeys frame for our app."""

    def __init__(self, parent, controller):
        # variables
        self.return_query = None
        self.decrypted_data = []
        customtkinter.CTkFrame.__init__(self, parent)
        # buttons
        button = customtkinter.CTkButton(self, text="SHOW JOURNEYS", command=lambda: self.run_query())
        button.grid(row=1, column=3, pady=5)

        return_menu = customtkinter.CTkButton(self, text="RETURN TO MAIN MENU",
                                              command=lambda: controller.show_frame(mainpage.MainPage))
        return_menu.grid(row=2, column=3, pady=5)

    def run_query(self):
        """This funtion will return all the user's trips."""
        # create cursor and connect to database
        cwd = os.getcwd()
        sqlite_file = cwd + r"/project_files/database_project.db"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()
        # for executing queries with foreign keys
        cursor.execute("""PRAGMA foreign_keys=ON;""")
        # run query
        sql = ("select start, finish, distance, activity_type, "
               f"duration, elevation, city, nonce_start, nonce_finish, "
               f"nonce_activity_type, nonce_city from bike_routes where username=?;")
        cursor.execute(sql, [get_value()])
        self.return_query = cursor.fetchall()
        #  create headers (entries) for each of the attributes
        attribute_names = ["start", "finish", "distance(kilometers)", "activity type", "duration(hours)",
                           "elevation(meters)", "city"]
        string_var_items = []
        for item in attribute_names:
            string_var_items.append(customtkinter.StringVar(self, f"{item}"))

        for i in range(len(attribute_names)):
            entry = customtkinter.CTkEntry(self, textvariable=string_var_items[i], state="readonly")
            entry.grid(row=3, column=i)
        # display the decrypted data
        if len(self.return_query) > 0:
            self.decrypt_data()
            i = 4
            for item in self.decrypted_data:
                for j in range(len(item)):
                    label = customtkinter.CTkLabel(self, text=f"{item[j]}")
                    label.grid(row=i, column=j)
                i += 1

    # noinspection SpellCheckingInspection
    def decrypt_data(self):
        """This funtion will decrypt the query data."""
        # initialize the list as empy so there are no repeated rows when the button is clicked multiple times
        self.decrypted_data = []
        # create chacha with global key
        key = get_encryption_key()
        chacha = ChaCha20Poly1305(key)

        # loop for decrypting items
        for item in self.return_query:
            decrypted_items = {"start": None, "finish": None, "distance": None,
                               "activity type": None, "duration": None, "elevation": None, "city": None}
            # first get nonces
            nonces_list = self.get_nonces(item)
            # now decrypt items
            decrypted_items["start"] = chacha.decrypt(nonces_list[0], item[0], None).decode()
            decrypted_items["finish"] = chacha.decrypt(nonces_list[1], item[1], None).decode()
            decrypted_items["distance"] = item[2]
            decrypted_items["activity type"] = chacha.decrypt(nonces_list[2], item[3], None).decode()
            decrypted_items["duration"] = item[4]
            decrypted_items["elevation"] = item[5]
            decrypted_items["city"] = chacha.decrypt(nonces_list[3], item[6], None).decode()
            decrypted_items_list = []
            # add them to a list
            for i in decrypted_items.values():
                decrypted_items_list.append(i)
            # add the decrytped items list to the main list
            self.decrypted_data.append(decrypted_items_list)

    def get_nonces(self, tuple_item):
        """This funtion will return the nonce's from the query."""
        nonce_list = []
        for i in range(7, 11):
            nonce_list.append(tuple_item[i])

        return nonce_list
