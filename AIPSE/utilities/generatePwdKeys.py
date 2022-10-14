for Stremalit logging module

import pickle
import pathlib as Path
import streamlit_authenticator as stauth

names = ["Peter Parker", "Rebecca Miller"]
usernames = ["pparker", "rmiller"]
passwords = ["abc123", "def456"]
credentials = {"usernames": {}}

for uname, name, pwd in zip(usernames, names, passwords):
    user_dict = {"name": name, "password": pwd}
    credentials["usernames"].update({uname: user_dict})

hashed_passwords = stauth.Hasher(passwords).generate()  # hasher uses bcrypt hashing

file_path = Path.Path('../', "hashed_pwd.pkl")
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)