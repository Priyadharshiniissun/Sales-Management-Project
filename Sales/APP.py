import streamlit as st



st.set_page_config(
    page_title="Login page",
    page_icon="🔐",
    layout="wide"
)

import streamlit as st

users = {
    "superadmin": {
        "password": "super123",
        "role": "Super Admin",
        "branch_id": None
    },

    "admin_chennai": {
        "password": "admin123",
        "role": "Admin",
        "branch_id": 1   
    },
      "admin_bangalore": {
        "password": "admin123",
        "role": "Admin",
        "branch_id": 2   
    },
     "admin_hyderabad": {
        "password": "admin123",
        "role": "Admin",
        "branch_id": 3   
    },
     "admin_delhi": {
        "password": "admin123",
        "role": "Admin",
        "branch_id": 4   
    },
     "admin_mumbai": {
        "password": "admin123",
        "role": "Admin",
        "branch_id": 5   
    },
     "admin_pune": {
        "password": "admin123",
        "role": "Admin",
        "branch_id": 6   
    },
     "admin_kolkata": {
        "password": "admin123",
        "role": "Admin",
        "branch_id": 7   
    },
     "admin_ahmedabad": {
        "password": "admin123",
        "role": "Admin",
        "branch_id": 8   
    }
}

st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    if username in users:

        if users[username]["password"] == password:

            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.session_state.branch_id = users[username]["branch_id"]

           
            if st.session_state.role == "Super Admin":

                st.switch_page("pages/super_admin.py")

            else:

                st.switch_page("pages/admin.py")

        else:
            st.error("Wrong Password")

    else:
        st.error("User Not Found")
