import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from utils.paths import BOOKS_PATH

def show_data_exploration():
    st.title("Eksploracja Danych")

    st.markdown("""
    W tej sekcji wykonamy analizę eksploracyjną danych, aby lepiej zrozumieć, jakie informacje można uzyskać z dostępnych zbiorów danych o książkach oraz autorach.

    - Sprawdzimy rozkład ocen książek.
    - Zobaczymy zależności między liczbą osób, które posiadają książkę a jej oceną.
    - Zobaczymy rozkład liczby stron w książkach w zależności od kategorii.
    """)

    try:
        books_df = pd.read_csv(BOOKS_PATH)

        # Wywołanie funkcji do rysowania wykresu KDE dla liczby stron w zależności od kategorii
        show_number_of_pages_based_on_category(books_df)

    except Exception as e:
        st.error(f"Error loading data: {e}")

def show_number_of_pages_based_on_category(books_df):
    # Usuwamy brakujące dane w kolumnach 'Kategoria' i 'Liczba stron'
    plot_data = books_df.dropna(subset=['Kategoria', 'Liczba stron'])

    # Filtrowanie kategorii, które mają więcej niż 0 książek
    filtered_categories_number = plot_data['Kategoria'].value_counts()
    filtered_categories = filtered_categories_number[filtered_categories_number > 0].index

    # Wybór kategorii przez użytkownika
    selected_categories = st.multiselect(
        "Wybierz kategorie książek do wyświetlenia:",
        options=filtered_categories,
        default=filtered_categories[:3]  # Domyślnie wyświetlamy pierwsze 3 kategorie
    )

    if selected_categories:
        # Filtrujemy dane dla wybranych kategorii
        plot_data_filtered = plot_data[plot_data['Kategoria'].isin(selected_categories)]

        # Rysowanie wykresu KDE dla każdej z wybranych kategorii
        fig, ax = plt.subplots(figsize=(15, 10))  # Tworzymy obiekt figury i osi
        for category in selected_categories:
            subset = plot_data_filtered[plot_data_filtered['Kategoria'] == category]
            sns.kdeplot(subset['Liczba stron'], ax=ax, label=category, fill=True, alpha=0.5)

        ax.set_title('Rozkład Jądrowy Liczby Stron w Książkach w Zależności od Kategorii')
        ax.set_xlabel('Liczba stron')
        ax.set_ylabel('Gęstość')
        ax.legend()
        st.pyplot(fig)  # Przekazujemy obiekt figury do st.pyplot()
    else:
        st.warning("Proszę wybrać przynajmniej jedną kategorię.")
