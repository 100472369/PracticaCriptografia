# here we define the global variables we are going to use


"""this will be the  key used to encrypt our data it will be different for
each user and will only be used when running the program."""
encryption_key = b''


def get_encryption_key():
    return encryption_key


def set_encryption_key(new_value):
    global encryption_key
    encryption_key = new_value


# variable used to access foreign key data
username_global = ""


def set_value(new_value):
    global username_global
    username_global = new_value


def get_value():
    return username_global
