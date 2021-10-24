""" Streamlit app for landing page"""

import webbrowser

import streamlit as st
from pages import main_page, about_page


st.set_page_config(
    page_title="VaXTrack",
    page_icon="data/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"

 )

st.sidebar.image("data/logo.png")

col1, col2, col3, col4 = st.sidebar.columns(4)
home_flag = col1.button('Home')
about_flag = col2.button('About')
presentation_flag = col3.button('Presentation')


col1, col2, col3, col4 = st.sidebar.columns(4)
report_flag = col1.button('Report')
datafolio_flag = col2.button('Datafolio')

st.empty()

st.sidebar.markdown("""
<a href=https://www.correlation-one.com/data-science-for-all-women> <img 
style="float: right;" 
src="https://www.correlation-one.com/hubfs/Colored
%20logo@2x.png"  width = 200/> </a>
""", unsafe_allow_html=True)


if about_flag:
    about_page()
elif presentation_flag:
    st.video('https://www.youtube.com/watch?v=Pna6PxUvloo')
elif datafolio_flag:
    st.image("data/datafolio-1.png")
elif report_flag:
    url = "https://drive.google.com/file/d/1QLk03WWv2zjC4DRB6k6tikT0fMth3muM/view?usp=sharing"
    webbrowser.open_new_tab(url)
else:
    main_page()
