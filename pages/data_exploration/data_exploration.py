import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import pandas as pd

from utils.paths import BOOKS_PATH, UMAP_BESTSELLERS_PATH, UMAP_CLUSTERS_PATH

def show_data_exploration():
    st.title("Eksploracja Danych")

    st.markdown("""
    W tej sekcji dokonamy analizy eksploracyjnej danych, aby lepiej zrozumieć informacje, które możemy wyciągnąć z dostępnych zbiorów danych o książkach oraz autorach. 

    Zaczniemy od analizy **rozkładu ocen książek**, aby zobaczyć, jak użytkownicy oceniają książki na platformie. Następnie przyjrzymy się **zależności między liczbą osób, które posiadają książkę, a jej oceną**, aby zrozumieć, jak popularność książek może wpływać na ich oceny.

    Kolejnym krokiem będzie **rozważenie rozkładu liczby stron w książkach w zależności od kategorii**. Dzięki temu będziemy mogli zobaczyć, jak różne kategorie książek różnią się pod względem liczby stron.

    Na koniec, zaprezentujemy wyniki analizy **UMAP 3D**, które pomogą zobrazować książki klasyfikowane jako **bestsellery** oraz **nie-bestsellery** w przestrzeni 3D. Dodatkowo, zobaczymy wyniki **UMAP dla grup klastrów**, które pokazują, jak książki są pogrupowane w różne klastry w zależności od ich cech.

    - Sprawdzimy **rozklad ocen książek**.
    - Zobaczymy zależności **między liczbą osób, które posiadają książkę a jej oceną**.
    - Zbadamy **rozkład liczby stron w książkach w zależności od kategorii**.
    - Zobaczymy **wyniki analizy UMAP dla bestsellerów i nie-bestsellerów oraz klastrów książek**.
    """)

    try:
        books_df = pd.read_csv(BOOKS_PATH)
        umap_bestseller_df = pd.read_csv(UMAP_BESTSELLERS_PATH)
        umap_clusters_df = pd.read_csv(UMAP_CLUSTERS_PATH)
        st.header('Rozkłady jądrowe liczby stron w książkach w zależności od kategorii')
        
        show_number_of_pages_based_on_category(books_df)

        st.header('Wykres UMAP 3D dla klas Bestsellery i Nie-Bestsellery')
        bestseller_title = "UMAP 3D - Bestsellery"
        show_umap_plot(umap_bestseller_df, title=bestseller_title)

        st.header('Pogrupowane Klastry')
        st.markdown("""
        Grupowanie książek w klastry medodą KNN.
        """)
        cluster_title = "UMAP 3D - Klastry"
        show_umap_plot(umap_clusters_df, title=cluster_title)

    except Exception as e:
        st.error(f"Error loading data: {e}")

def show_number_of_pages_based_on_category(books_df):
    
    plot_data = books_df.dropna(subset=['Kategoria', 'Liczba stron'])

    
    filtered_categories_number = plot_data['Kategoria'].value_counts()
    filtered_categories = filtered_categories_number[filtered_categories_number > 0].index

    
    selected_categories = st.multiselect(
        "Wybierz kategorie książek do wyświetlenia:",
        options=filtered_categories,
        default=filtered_categories[:3]
    )

    if selected_categories:

        plot_data_filtered = plot_data[plot_data['Kategoria'].isin(selected_categories)]


        fig, ax = plt.subplots(figsize=(15, 10))
        for category in selected_categories:
            subset = plot_data_filtered[plot_data_filtered['Kategoria'] == category]
            sns.kdeplot(subset['Liczba stron'], ax=ax, label=category, fill=True, alpha=0.5)

        ax.set_title('Rozkład Jądrowy Liczby Stron w Książkach w Zależności od Kategorii')
        ax.set_xlabel('Liczba stron')
        ax.set_ylabel('Gęstość')
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Proszę wybrać przynajmniej jedną kategorię.")

def show_umap_plot(umap_df, title="UMAP 3D"):
    target_col = umap_df.columns[-1]
    fig = px.scatter_3d(umap_df, x="UMAP1", y="UMAP2", z="UMAP3", 
                        color=umap_df.iloc[:, -1].astype(str),
                        title=title,
                        labels={"color": target_col},
                        opacity=0.7)
    fig.update_layout(width=800, height=600)

    st.plotly_chart(fig)