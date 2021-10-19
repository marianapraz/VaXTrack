""" Streamlit app for landing page"""

import base64

import streamlit as st
from pages import main_page, about_page


st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/a/ab"
               "/Logo_TV_2015.png",
    layout="wide",
    initial_sidebar_state="expanded"

 )

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/a/ab"
               "/Logo_TV_2015.png")

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
    st.video('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
elif datafolio_flag:
    st.image("data:image/jpeg;base64,"
             "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")
elif report_flag:
    with open('data/report.pdf', "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
else:
    main_page()
