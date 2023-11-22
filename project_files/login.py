# general use functions
import sqlite3
import os
import cryptography.exceptions
import customtkinter
# frames and global variable access functions
from signup import SignUp
from mainpage import MainPage
from settings import set_value, set_encryption_key, get_value
# used for verifying derived password and for creating encryption key
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
# used for signature creation and verification
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import PublicFormat, PrivateFormat, BestAvailableEncryption
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
# used for generating and verifying certificates
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.serialization import Encoding
import subprocess


class Login(customtkinter.CTkFrame):
    """This is the login frame for our app."""
    def __init__(self, parent, controller):
        # variables
        self.data = []

        customtkinter.CTkFrame.__init__(self, parent)
        # this is used to center all the elements
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(4, weight=2)

        # labels, entries and buttons

        label = customtkinter.CTkLabel(self, text="Login Page", font=("Impact", 25))
        label.grid(row=1, column=2, pady=(155, 5))

        label_username = customtkinter.CTkLabel(self, text="Username:", font=("Trebuchet MS", 15))
        label_username.grid(row=2, column=1, pady=5)

        entry_username = customtkinter.CTkEntry(self, placeholder_text="username", font=("Trebuchet MS", 15))
        entry_username.grid(row=2, column=2, pady=5)
        self.data.append(entry_username)

        label_password = customtkinter.CTkLabel(self, text="Password: ", font=("Trebuchet MS", 15))
        label_password.grid(row=3, column=1, pady=2)

        entry_password = customtkinter.CTkEntry(self, placeholder_text="password", show="*", font=("Trebuchet MS", 15))
        entry_password.grid(row=3, column=2, pady=2)
        self.data.append(entry_password)

        login_button = customtkinter.CTkButton(self, text="Login", text_color="#3E4B3C", command=lambda: self.log_user
            (controller, incorrect_data), fg_color="#91D53E", hover_color="#689F33", border_color="#3E4B3C", height=30,
                                               border_width=1)
        login_button.grid(row=4, column=2, pady=2)

        sign_up_button = customtkinter.CTkButton(self, text="Sign up", text_color="#3E4B3C",
                                                 command=lambda: controller.show_frame(SignUp),
                                                 fg_color="#91D53E", hover_color="#689F33", border_color="#3E4B3C",
                                                 height=30, border_width=1)
        sign_up_button.grid(row=5, column=2, pady=2)

        incorrect_data = customtkinter.CTkLabel(self, text="INCORRECT USERNAME OR PASSWORD", text_color="red")

    def log_user(self, controller, label):
        """this function will try to log the user and redirect to the main page.
        If not possible it wil display a red label error."""
        # initiate sql data
        cwd = os.getcwd()
        sqlite_file = cwd + r"/project_files/database_project.db"
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()

        # execute query
        sql = "select username, password, salt_password, salt_key FROM users where username=?"
        cursor.execute(sql, [self.data[0].get()])

        # check if user exists
        database_tuple = cursor.fetchall()
        if len(database_tuple) == 0:
            label.grid(row=6, column=1, columnspan=2)
            return None
        # verify entered password
        try:
            salt = database_tuple[0][2]
            kdf = self.generate_kdf(salt)

            kdf.verify(self.data[1].get().encode(), database_tuple[0][1])
        except cryptography.exceptions.InvalidKey:
            label.grid(row=6, column=1, columnspan=2)

        else:
            # set username value
            set_value(self.data[0].get())
            # create signature
            self.sign_username(controller, conn, cursor)
            # verify signature
            self.verify_signature(cursor, controller)
            # obtain certificate
            self.obtain_certificate(cursor, controller)
            # verify certificate
            self.verify_certificate(controller)
            # close sqlite cursor
            cursor.close()
            # remove text from entries
            for item in self.data:
                item.delete(0, "end")
            # create key for accessing data
            salt = database_tuple[0][3]
            kdf = self.generate_kdf(salt)

            # store key as temporary global variable
            key = kdf.derive(self.data[1].get().encode())
            set_encryption_key(key)

            #  write verification message log
            messages = [f"Login information for user: {get_value()}",
                        "Successfully verified user data.", "Algorithm used: Scrypt. Length of key: 32\n"]
            controller.write_log(messages)

            # show main page
            controller.show_frame(MainPage)

    def generate_kdf(self, salt):
        """This funtion is used to generate a kdf object with a salt passed as parameter."""
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2 ** 14,
            r=8,
            p=1,
        )
        return kdf

    def sign_username(self, controller, conn, cursor):
        """This funtion will create a signature for the user and insert it into the database. """
        # sql initialize
        # create table
        sql = """create table if not exists signature
            (
                username   TEXT
                    constraint signature_users_username_fk
                        references users
                        on update cascade on delete cascade,
                public_key BLOB not null,
                signature  BLOB not null
            );"""
        cursor.execute(sql)
        try:
            # generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            # generate byte message
            message = get_value().encode("utf-8")
            # generate signature
            signature = self.create_signature(private_key, message)
            # generate public key object
            public_key = private_key.public_key()
            # serialization of public key
            public_key_string = public_key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)
            # serialization of private key
            private_key_string = private_key.private_bytes(encoding=Encoding.PEM,
                                                           format=PrivateFormat.TraditionalOpenSSL,
                                      encryption_algorithm=BestAvailableEncryption(self.data[1].get().encode()))
            # insertion into database
            sql = """INSERT INTO signature (username, public_key, signature, private_key) VALUES (?, ?, ?, ?)"""
            cursor.execute(sql, [get_value(), public_key_string, signature, private_key_string])
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        # write signature creation message in log
        messages = [f'Login information for user: {get_value()}',
                    "Successfully signed username value",
                    "Algorithms used: RSA. Length of key: 2048 B\n"]
        controller.write_log(messages)

    def create_signature(self, private_key, message):
        """This function will create a signature given a private key and a message as parameters."""
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def verify_signature(self, cursor, controller):
        """This funtion will verify the user's signature."""
        # get the signature data with sqlite3 query
        sql = """select username, public_key, signature from signature where username=?;"""
        cursor.execute(sql, [get_value()])
        data = cursor.fetchone()
        # get appropriate data
        message = data[0].encode(encoding="UTF-8")
        public_key = load_pem_public_key(data[1])
        signature = data[2]
        # execute signature verification
        try:
            public_key.verify(signature,
                              message,
                              padding.PSS(
                                  mgf=padding.MGF1(hashes.SHA256()),
                                  salt_length=padding.PSS.MAX_LENGTH
                              ),
                              hashes.SHA256()
                              )
            # write signature verification message in log
            messages = [f"Login information for user: {get_value()}",
                        "Successfully verified signature.", "Algorithm used: RSA. \n"]
            controller.write_log(messages)

        except cryptography.exceptions.InvalidSignature:
            # write verification failure in log
            messages = [f"Login information for user: {get_value()}",
                        "Signature verification failed.",
                        "Check if user has signature entry in signature table of database. \n"]
            controller.write_log(messages)

    def obtain_certificate(self, cursor, controller):
        """This function will create a x509 certificate for the user."""
        # get the signature data with sqlite3 query
        sql = """select username, public_key, signature, private_key from signature where username=?;"""
        cursor.execute(sql, [get_value()])
        data = cursor.fetchone()
        # get private key
        private_key = load_pem_private_key(data=data[3], password=self.data[1].get().encode())
        # Generate a CSR
        csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
            # Provide various details about who we are.
            x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Madrid"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Madrid"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Bicycle Land"),
            x509.NameAttribute(NameOID.COMMON_NAME, f"{get_value()}"),
        ])).add_extension(
            x509.SubjectAlternativeName([
                # Describe what sites we want this certificate for.
                x509.DNSName("bicycleland.com"),
                x509.DNSName("www.bicycleland.com"),
                x509.DNSName("subdomain.bicycleland.com"),
            ]),
            critical=False,
            # Sign the CSR with our private key.
        ).sign(private_key, hashes.SHA256())
        # Write our CSR out to disk.
        path = os.getcwd() + f"/A/{get_value()}req.pem"
        with open(f"{path}", "wb") as f:
            f.write(csr.public_bytes(Encoding.PEM))

        # turn the request into a certificate with openssl
        source_path = os.getcwd()
        # route to the file in case it already exists
        file = source_path + f"/A/{get_value()}cert.pem"
        nuevos_certs = source_path + "/AC2/nuevoscerts"
        if not os.path.exists(nuevos_certs):
            os.makedirs(nuevos_certs)
        # create nuevoscerts if it does not exist
        if not os.path.exists(file):
            # run openssl commands
            subprocess.run(f'cd {source_path}/AC2; openssl ca -in ../A/{get_value()}req.pem -notext -config ./openssl_AC2-461170.cnf', shell=True)
            subprocess.run(f'mv {source_path}/AC2/nuevoscerts/* {source_path}/AC2/nuevoscerts/{get_value()}cert.pem', shell=True)
            subprocess.run(f'mv {source_path}/AC2/nuevoscerts/{get_value()}cert.pem {source_path}/A', shell=True)

        # write certificate generation message in log
        messages = [f"Login information for user: {get_value()}",
                    "Successfully generated user certificate.", "Created using x509 and OpenSSL. \n"]
        controller.write_log(messages)

    def verify_certificate(self, controller):
        """This function will perform the chain validation of the certificates."""
        path = os.getcwd()
        # certify A
        subprocess.run(f'cd {path}/A; openssl verify -CAfile certs.pem {get_value()}cert.pem', shell=True)
        # certify AC2
        subprocess.run(f'cd {path}/AC2; openssl verify -CAfile ../AC1/ac1cert.pem ac2cert.pem', shell=True)
        # certify AC1
        subprocess.run(f'cd {path}/AC1; openssl verify -CAfile ac1cert.pem ac1cert.pem', shell=True)
        # write certification message in log
        messages = [f"Login information for user: {get_value()}",
                    "Successfully validated user certificate.", "Achieved using OpenSSL commands.\n"]
        controller.write_log(messages)
