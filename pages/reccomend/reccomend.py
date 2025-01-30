import streamlit as st
import pandas as pd
import joblib

# Ładowanie modeli z plików .pkl
def load_models():
    log_reg = joblib.load('data/models/randomized_log_reg.pkl')
    random_forest = joblib.load('data/models/random_forrest_grid.pkl')
    knn = joblib.load('data/models/knn_grid.pkl')
    return log_reg, random_forest, knn

# Funkcja do predykcji na zbiorze testowym
def predict_books(models, books_df, test_features, y_test):
    log_reg, random_forest, knn = models
    X_logreg, X_forrest, X_knn = test_features

    # Predykcje dla każdego modelu
    log_reg_preds = log_reg.predict(X_logreg)
    rf_preds = random_forest.predict(X_forrest)
    knn_preds = knn.predict(X_knn)

    # Filtrowanie książek, które są klasyfikowane jako niedocenione (model przewiduje je jako bestseller, ale y == 0)
    underrated_books_logreg = books_df[(y_test == 0) & (log_reg_preds == 1)]
    underrated_books_rf = books_df[(y_test == 0) & (rf_preds == 1)]
    underrated_books_knn = books_df[(y_test == 0) & (knn_preds == 1)]

    # Sortowanie książek po liczbie osób, które ją posiadają
    underrated_books_logreg_sorted = underrated_books_logreg.sort_values('number_of_people_has', ascending=False).head(20)
    underrated_books_rf_sorted = underrated_books_rf.sort_values('number_of_people_has', ascending=False).head(20)
    underrated_books_knn_sorted = underrated_books_knn.sort_values('number_of_people_has', ascending=False).head(20)

    return underrated_books_logreg_sorted, underrated_books_rf_sorted, underrated_books_knn_sorted

def load_features():
    X_test_logreg = pd.read_csv('data/models/X_test.csv')
    X_test_forrest = pd.read_csv('data/models/X_test_forrest.csv')
    X_test_knn = pd.read_csv('data/models/X_test_knn.csv')

    return X_test_logreg, X_test_forrest, X_test_knn

# Strona Streamlit
def show_random_books():
    st.title("Losowanie Książek Niedocenionych")

    # Ładowanie modeli
    models = load_models()
    test_features = load_features()

    # Wczytanie danych o książkach
    books_df = pd.read_csv('data/books_data.csv')  # Zakładając, że masz plik CSV z danymi o książkach
    books_df['title'] = books_df['url'].str.split('/').str[-1].str.split('-').str.join(' ').str.title()
    books_df['number_of_people_has'] = books_df['number_of_people_has'].fillna(0).astype(int)

    # Zakładając, że masz odpowiednią zmienną `y_test` (czy książka to bestseller czy nie)
    # Jeśli nie masz jej w zbiorze, musisz to przygotować wcześniej
    y_test = pd.read_csv('data/models/y_bestsellers.csv')


    # Losowanie książek dla każdego modelu
    random_logreg_books, random_rf_books, random_knn_books = predict_books(models, books_df, test_features, y_test)

    # Wyświetlanie losowo wybranych książek dla każdego modelu
    st.subheader("Losowe książki według modelu Regresji Logistycznej")
    st.write(random_logreg_books[['title', 'author', 'number_of_people_has']])

    st.subheader("Losowe książki według modelu Random Forest")
    st.write(random_rf_books[['title', 'author', 'number_of_people_has']])

    st.subheader("Losowe książki według modelu KNN")
    st.write(random_knn_books[['title', 'author', 'number_of_people_has']])

if __name__ == "__main__":
    show_random_books()
