import streamlit as st

def thank_you():
    st.title("Thank You!")
    
    st.write("Thank you for using our services!")
    
    # Team member information
    team_members = {
        "Vinayak": "Project Manager & ML Engineer",
        "Digvijay": "Lead Developer & Tester ",
        "Suhas":  " Document Controller & Devoloper",
        "Chinmayee": "UI/UX Designer & AI Engineer"
    }
    
    st.subheader("Team Members:")
    
    for name, role in team_members.items():
        st.write(f"{name}: {role}")

if __name__ == "__main__":
    thank_you()
