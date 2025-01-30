import streamlit as st
import matplotlib.pyplot as plt
from plotly import express as px
import seaborn as sns
import pandas as pd

from utils.paths import BOOKS_PATH

def show_data_exploration():
    st.title("Eksploracja Danych")

    st.markdown("""
    W tej sekcji wykonamy analizę eksploracyjną danych, aby lepiej zrozumieć, jakie informacje można uzyskać z dostępnych zbiorów danych o książkach oraz autorach.

    - Sprawdzimy rozkład ocen książek.
    - Zobaczymy zależności między liczbą osób, które posiadają książkę a jej oceną.
    """)

    try:
        books_df = pd.read_csv(BOOKS_PATH)
        # Przykład wykresu rozkładu ocen książek
        st.subheader("Rozkład ocen książek")
        plt.figure(figsize=(10, 6))
        # sns.histplot(books_df['rating_10'], kde=True, bins=30)
        plt.title("Rozkład ocen 10")
        st.pyplot()

        # Zależność między liczbą osób posiadających książkę a oceną
        st.subheader("Zależność między liczbą osób posiadających książkę a oceną")
        plt.figure(figsize=(10, 6))

        plt.title("Liczba osób posiadających książkę vs Ocena")
        st.pyplot()

    except Exception as e:
        st.error(f"Error loading data: {e}")


def show_number_of_pages_based_on_category(books_df):
    plot_data = books_df.dropna(subset=['Kategoria', 'Liczba stron'])
    filtered_categories_number = plot_data['Kategoria'].value_counts()
    filtered_categories = filtered_categories[filtered_categories_number > 800].index
    plt.figure(figsize=(15, 10))
    for category in filtered_categories:
        subset = plot_data[plot_data['Kategoria'] == category]
        sns.kdeplot(subset['Liczba stron'], label=category, fill=True, alpha=0.5)

    plt.title('Rozkład Jądrowy Liczby Stron w Książkach w Zależności od Kategorii')
    plt.xlabel('Liczba stron')
    plt.ylabel('Density')
    plt.legend()
    plt.show()