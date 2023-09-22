# here we define the global variables we are going to use

username_global = ""


def set_value(new_value):
    global username_global
    username_global = new_value

def get_value():
    return username_global