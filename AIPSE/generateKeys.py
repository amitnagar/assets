#for Streamlit logging module

import pickle
import pathlib as Path

import streamlit_authenticator as stauth


if __name__ == "__main__":
    names = ["Peter Parker", "Rebecca Miller", "Amit"]
    usernames = ["pparker", "rmiller", "amit"]
    passwords = ["xxxx", "xxxx", "xxxx"]

    credentials = {"usernames": {}}

    for uname, name, pwd in zip(usernames, names, passwords):
        user_dict = {"name": name, "password": pwd}
        credentials["usernames"].update({uname: user_dict})

    hashed_passwords = stauth.Hasher(passwords).generate()  # hasher uses bcrypt hashing

    file_path = Path.Path('./', "hashed_pwd.pkl")
    with file_path.open("wb") as file:
        pickle.dump(hashed_passwords, file)
