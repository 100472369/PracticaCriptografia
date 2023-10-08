import customtkinter
import os
import sqlite3
import main_page
from settings import get_value, get_encryption_key
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

class View_journeys(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        self.return_query = None
        self.decrypted_data = []
        customtkinter.CTkFrame.__init__(self, parent)
        button = customtkinter.CTkButton(self, text="SHOW JOURNEYS", command=lambda:self.run_query())
        button.grid(row=1, column=3, pady=5)

        return_menu = customtkinter.CTkButton(self, text="RETURN TO MAIN MENU",
                                              command=lambda: controller.show_frame(main_page.Main_page))
        return_menu.grid(row=2, column=3, pady=5)

    def run_query(self):
        rows = None
        columns = None


        cwd = os.getcwd()
        sqlite_file = cwd + r"/database_project"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()
        # for executing queries with foreign keys
        cursor.execute("""PRAGMA foreign_keys=ON;""")

        sql = ("select start, finish, distance, activity_type, "
               f"duration, elevation, city, nonce_start, nonce_finish, "
               f"nonce_activity_type, nonce_city from bike_routes where username=?;")
        cursor.execute(sql, [get_value()])
        self.return_query = cursor.fetchall()


        attribute_names = ["start", "finish", "distance(kilometers)", "activity type", "duration(hours)", "elevation(meters)", "city"]
        string_var_items = []
        for item in attribute_names:
            string_var_items.append(customtkinter.StringVar(self, f"{item}"))




        for i in range(len(attribute_names)):
            entry = customtkinter.CTkEntry(self, textvariable=string_var_items[i], state="readonly")
            entry.grid(row =3, column=i)


        if len(self.return_query) > 0:
            self.decrypt_data()
            i = 4
            for item in self.decrypted_data:
                for j in range(len(item)):
                    label = customtkinter.CTkLabel(self, text=f"{item[j]}")
                    label.grid(row=i, column=j)
                i += 1



    def decrypt_data(self):
        self.decrypted_data = []
        key = get_encryption_key()
        chacha = ChaCha20Poly1305(key)

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

            for i in decrypted_items.values():
                decrypted_items_list.append(i)

            self.decrypted_data.append(decrypted_items_list)

    def get_nonces(self, tuple_item):
        nonce_list = []
        for i in range(7, 11):
            nonce_list.append(tuple_item[i])

        return nonce_list




