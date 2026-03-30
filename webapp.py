import streamlit as st

# Title and icon for all pages 
st.set_page_config(
    page_title="CivilEngineeringTools",
    page_icon="🧱",
    layout="wide"
)

# Configure Pages 

levellinG=st.Page(
    page="streamlit_pages/levelling.py",
    title="Levelling Automation",
    icon="💠"
)
traversE=st.Page(
    page="streamlit_pages/traverse.py",
    title="Traverse Automation",
    icon="💠"
)
developeR=st.Page(
    page="streamlit_pages/developer.py",
    title="Developer",
    icon="👨‍💻",
    default=True
)

# naviagtion
nav = st.navigation(
    {
        "Tools":[levellinG,traversE],
        "Info":[developeR]
    }
)
# run the navigation
nav.run()

# Shared on nav bar on all pages 
st.sidebar.markdown("Made with 💌 by Shivam")