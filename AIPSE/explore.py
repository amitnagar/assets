import streamlit as st
import pandas as pd
import numpy as np

import pickle
import pathlib as Path
import streamlit_authenticator as stauth

import search

if __name__ == "__main__":
    names = ['Peter Parker', 'Rebecca Miller', 'Amit']
    usernames = ['pparker', 'rmiller', 'amit']

    file_path = Path.Path('./', "hashed_pwd.pkl")
    with file_path.open("rb") as file:
        passwords = pickle.load(file)

    credentials = {"usernames": {}}

    for uname, name, pwd in zip(usernames, names, passwords):
        user_dict = {"name": name, "password": pwd}
        credentials["usernames"].update({uname: user_dict})

    authenticator = stauth.Authenticate(credentials, "cookie_name", "hashkey_abcdef", cookie_expiry_days=30)

    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status == False:
        st.error("login failed")

    if authentication_status == None:
        st.warning("please enter username, password")

    if authentication_status:
        search.search()
#