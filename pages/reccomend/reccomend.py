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
def predict_books(models, books_df, test_features, y_test, number_of_books=10):

    log_reg, random_forest, knn = models
    X_logreg, X_forrest, X_knn = test_features

    # Predykcje dla każdego modelu
    log_reg_preds = log_reg.predict(X_logreg)
    log_reg_pred_series = pd.Series(log_reg_preds, index=X_logreg.index)
    rf_preds = random_forest.predict(X_forrest)
    rf_pred_series = pd.Series(rf_preds, index=X_forrest.index)
    knn_preds = knn.predict(X_knn)
    knn_pred_series = pd.Series(knn_preds, index=X_knn.index)

    # Filtrowanie książek, które są klasyfikowane jako niedocenione (model przewiduje je jako bestseller, ale y == 0)
    y_test_log_reg = y_test.loc[X_logreg.index, 'bestseller']
    y_test_rf = y_test.loc[X_forrest.index, 'bestseller']
    y_test_knn = y_test.loc[X_knn.index, 'bestseller']
    underrated_books_logreg = books_df.loc[y_test_log_reg.index[((y_test_log_reg == 0).T & (log_reg_pred_series == 1)).T]]
    underrated_books_rf = books_df.loc[y_test_rf.index[((y_test_rf == 0).T & (rf_pred_series == 1)).T]]
    underrated_books_knn = books_df.loc[y_test_knn.index[((y_test_knn == 0).T & (knn_pred_series == 1)).T]]

    # Sortowanie książek po liczbie osób, które ją posiadają
    legrog_cap = min(underrated_books_logreg.shape[0], number_of_books)
    rf_cap = min(underrated_books_rf.shape[0], number_of_books)
    knn_cap = min(underrated_books_knn.shape[0], number_of_books)
    underrated_books_logreg_sorted = underrated_books_logreg.sample(legrog_cap)
    underrated_books_rf_sorted = underrated_books_rf.sample(rf_cap)
    underrated_books_knn_sorted = underrated_books_knn.sample(knn_cap)

    return underrated_books_logreg_sorted, underrated_books_rf_sorted, underrated_books_knn_sorted

def load_features():
    X_test_logreg = pd.read_csv('data/models/X_test.csv', index_col=0)
    X_test_forrest = pd.read_csv('data/models/X_test_forrest.csv', index_col=0)
    X_test_knn = pd.read_csv('data/models/X_test_knn.csv', index_col=0)

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
    y_test = pd.read_csv('data/models/y_bestsellers.csv', index_col=0)


    # Losowanie książek dla każdego modelu
    random_logreg_books, random_rf_books, random_knn_books = predict_books(models, books_df, test_features, y_test)

    columns_to_show = ['title', 'author', 'number_of_people_has', 'description', 'ISBN']

    # Wyświetlanie losowo wybranych książek dla każdego modelu
    st.subheader("Losowe książki według modelu Regresji Logistycznej")
    st.write(random_logreg_books[columns_to_show])

    st.subheader("Losowe książki według modelu Random Forest")
    st.write(random_rf_books[columns_to_show])

    st.subheader("Losowe książki według modelu KNN")
    st.write(random_knn_books[columns_to_show])

if __name__ == "__main__":
    show_random_books()
