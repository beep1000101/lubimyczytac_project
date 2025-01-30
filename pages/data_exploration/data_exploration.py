import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def show_data_exploration():
    st.title("Eksploracja Danych")

    st.markdown("""
    W tej sekcji wykonamy analizę eksploracyjną danych, aby lepiej zrozumieć, jakie informacje można uzyskać z dostępnych zbiorów danych o książkach oraz autorach.

    - Sprawdzimy rozkład ocen książek.
    - Zobaczymy zależności między liczbą osób, które posiadają książkę a jej oceną.
    """)

    # Załaduj dane (np. z plików CSV lub DataFrame)
    try:
        # books_df = pd.read_csv('books_tmp1.csv')  # Wczytanie danych książek
        # authors_df = pd.read_csv('authors_tmp1.csv')  # Wczytanie danych autorów

        # Przykład wykresu rozkładu ocen książek
        st.subheader("Rozkład ocen książek")
        plt.figure(figsize=(10, 6))
        # sns.histplot(books_df['rating_10'], kde=True, bins=30)
        plt.title("Rozkład ocen 10")
        st.pyplot()

        # Zależność między liczbą osób posiadających książkę a oceną
        st.subheader("Zależność między liczbą osób posiadających książkę a oceną")
        plt.figure(figsize=(10, 6))
        # sns.scatterplot(x=books_df['number_of_people_has'], y=books_df['rating_10'])
        plt.title("Liczba osób posiadających książkę vs Ocena")
        st.pyplot()

    except Exception as e:
        st.error(f"Error loading data: {e}")
