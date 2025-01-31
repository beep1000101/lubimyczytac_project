import streamlit as st
import numpy as np

from pages.home import home
from pages.data_sourcing import data_sourcing
from pages.data_exploration import data_exploration
from pages.modeling import modeling
from pages.results import results
from pages.reccomend import reccomend

# Set the page configuration
st.set_page_config(
    page_title="Lubimyczytac Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def app():
    st.sidebar.title("Navigation")
    st.sidebar.markdown("Select a section:")
    section = st.sidebar.radio("Sections", ["Home", "Data Acquisition", "Data Exploration", "Modeling", 'Results', 'Recommend'])

    if section == "Home":
        home.show_home()
    elif section == "Prediction":
        st.title("Prediction Page")
        st.markdown("This is where the prediction model will go.")
    elif section == "About":
        st.title("About")
        st.markdown("This app classifies books based on data from lubimyczytac.pl.")
    elif section == "Data Acquisition":
        data_sourcing.show_data_acquisition()
    elif section == "Data Exploration":
        data_exploration.show_data_exploration()
    elif section == "Modeling":
        modeling.show_modeling()
    elif section == "Results":
        results.show_model_results()
    elif section == "Recommend":
        reccomend.show_random_books()

if __name__ == "__main__":
    app()
