import streamlit as st

# Set up session state for login status if not already done.
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Redirect to the login page by default.
if not st.session_state.logged_in:
    import login as login_page  # Importing the login page.
    login_page.login()
else:
    import pages.main as main_page  # Importing the main functionality page.
    main_page.main()
    import pages.thank_you as thank_you
    thank_you.thank_you()
