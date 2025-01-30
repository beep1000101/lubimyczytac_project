import streamlit as st
import numpy as np

from pages.home import home

def app():
    st.sidebar.title("Navigation")
    st.sidebar.markdown("Select a section:")
    st.sidebar.radio("Sections", ["Home", "Prediction", "About"])

    st.title(home.home_title)
    st.markdown(home.home_description)
    

if __name__ == "__main__":
    app()