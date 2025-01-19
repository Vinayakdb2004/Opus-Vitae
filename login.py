import streamlit as st
from database import create_connection, create_table, add_user, get_user

# Initialize database connection
conn = create_connection("users.db")
create_table(conn)

# Initialize session state for logged_in if it does not exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("Login / Sign Up Page")

    # Registration section
    st.subheader("Register")
    reg_username = st.text_input("New Username")
    reg_password = st.text_input("New Password", type='password')

    if st.button("Register"):
        if reg_username and reg_password:
            try:
                add_user(conn, reg_username, reg_password)
                st.success("User registered successfully!")
                st.session_state.logged_in = True  # Set logged_in to True
                st.experimental_rerun()  # Refresh to load the main menu
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please enter both username and password.")

    # Login section
    st.subheader("Login")
    
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type='password', key="login_password")

    if st.button("Login"):
        user = get_user(conn, username)
        if user and user[2] == password:  # Check if the password matches
            st.session_state.logged_in = True  # Set logged_in to True
            st.success("Login successful!")
            #st.experimental_rerun()  # Refresh to load the main menu
        else:
            st.error("Invalid username or password")

    # Redirect to main page if logged in
    if st.session_state.logged_in:
        import pages.main as main_page  # Importing the main functionality page.
        main_page.main()  # Call the main function to display it.

if __name__ == "__main__":
    login()
