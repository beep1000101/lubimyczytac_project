import streamlit as st
import numpy as np

from pages.home import home
from pages.data_sourcing import data_sourcing
from pages.data_exploration import data_exploration
from pages.modeling import modeling
from pages.results import results
from pages.reccomend import reccomend

st.set_page_config(
    page_title="Lubimyczytac Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def app():
    st.sidebar.title("Nawigacja")
    st.sidebar.markdown("Wybierz sekcję:")
    section = st.sidebar.radio("Sekcje", ["Strona Główna", "Pozyskiwanie Danych", "Eksploracja Danych", "Modelowanie", 'Wyniki', 'Rekomendacje'])

    match section:
        case "Strona Główna":
            home.show_home()
        case "Pozyskiwanie Danych":
            data_sourcing.show_data_acquisition()
        case "Eksploracja Danych":
            data_exploration.show_data_exploration()
        case "Modelowanie":
            modeling.show_modeling()
        case "Wyniki":
            results.show_model_results()
        case "Rekomendacje":
            reccomend.show_random_books()

if __name__ == "__main__":
    app()
