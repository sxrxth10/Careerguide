import streamlit as st
from modules.userdetails import userdetails
from modules.live_test import live_test
from modules.quiz import quiz





tab1, tab2, tab3, tab4, tab5 = st.tabs(["Instructions", "User Profile", "Aptitude test", "Quiz", "Domain Suggestion"])


with tab1:
    pass

with tab2:
    userdetails()

with tab3:
    live_test()

with tab4:
    quiz()

with tab5:
    pass

