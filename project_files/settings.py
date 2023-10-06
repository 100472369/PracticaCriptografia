# here we define the global variables we are going to use

#######################################################################################################################
"""this will be the  key used to encrypt our data"""
encryption_key =b'k\xd0\xea\xce\xf6\x14\xfcOH\xa7\x9a\x8c\xb2F\xca\x163K\x11\x8a\xa75\x88,.\x82P\xd6\x0e\xb4\x7fK'

def get_encryption_key():
    return encryption_key


#######################################################################################################################

# variable used to access foreign key data
username_global = ""

def set_value(new_value):
    global username_global
    username_global = new_value

def get_value():
    return username_global