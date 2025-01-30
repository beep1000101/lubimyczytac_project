import streamlit as st
import numpy as np

from pages.home import home
from pages.data_sourcing import data_sourcing  # Dodajemy import dla nowej strony

def app():
    st.sidebar.title("Navigation")
    st.sidebar.markdown("Select a section:")
    section = st.sidebar.radio("Sections", ["Home", "Prediction", "About", "Data Acquisition"])

    if section == "Home":
        home.show_home()
    elif section == "Prediction":
        st.title("Prediction Page")  # Dodaj stronę predykcji
        st.markdown("This is where the prediction model will go.")
    elif section == "About":
        st.title("About")  # Strona 'About'
        st.markdown("This app classifies books based on data from lubimyczytac.pl.")
    elif section == "Data Acquisition":
        data_sourcing.show_data_acquisition()  # Wywołujemy funkcję do pokazania strony o pozyskiwaniu danych

if __name__ == "__main__":
    app()
