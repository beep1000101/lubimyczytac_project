import streamlit as st

def show_data_acquisition():
    st.title("Pozyskiwanie Danych")

    st.markdown("""
    ## Jak pozyskiwałem dane?

    Aby zebrać dane, wykorzystałem język Python oraz dwie popularne biblioteki: **requests** oraz **BeautifulSoup**. 

    1. **requests** pozwala na wysyłanie zapytań HTTP do strony, a **BeautifulSoup** ułatwia parsowanie HTML. 
    2. Skorzystałem z metody inżynierii wstecznej, aby zidentyfikować odpowiednie zapytania HTTP umożliwiające iterowanie po stronach wyników wyszukiwania serwisu **lubimyczytac.pl**.
    3. Pętla iterowała od strony 1 do 344, zbierając linki do poszczególnych książek.
    4. Z każdego URL-a książki pobierałem szczegóły, takie jak: autor, oceny użytkowników, liczba opinii, kategorie itp.
    5. Dodatkowo, odwiedzałem strony autorów, aby pozyskać dane o nich, takie jak średnia ocena autora, liczba książek, liczba fanów i inne.

    ## Biblioteki użyte w procesie:

    - **requests**: do wysyłania zapytań HTTP.
    - **BeautifulSoup**: do parsowania HTML i ekstrakcji potrzebnych danych.

    ## Przykład kodu do pozyskiwania danych:

    ```python
    import requests
    from bs4 import BeautifulSoup

    base_url = "https://lubimyczytac.pl/ksiazki/podobne/"
    for page in range(1, 345):
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        # dalsze operacje na danych
    ```

    Dzięki temu procesowi udało się zebrać dane o książkach oraz autorach, które są wykorzystywane w modelu klasyfikacyjnym.
    """)
