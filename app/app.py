import streamlit as st
from modules.userdetails import userdetails
from modules.aptitude_test import aptitude_test
from modules.quiz import quiz
from modules.suggestion import final_suggestion_page
from modules.home import home_page




tab1, tab2, tab3, tab4, tab5 = st.tabs(["Instructions", "User Profile", "Aptitude test", "Quiz", "Domain Suggestion"])


with tab1:
    home_page()

with tab2:
    userdetails()

with tab3:
    aptitude_test()

with tab4:
    quiz()

with tab5:
    final_suggestion_page()

