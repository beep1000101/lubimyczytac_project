import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import random

def show_data_acquisition():
    st.title("Data Acquisition")

    st.markdown("""
    ## Jak pozyskiwałem dane?

    Aby zebrać dane, wykorzystałem język Python oraz dwie popularne biblioteki: **requests** oraz **BeautifulSoup**.

    1. **requests** pozwala na wysyłanie zapytań HTTP do strony, a **BeautifulSoup** ułatwia parsowanie HTML.
    2. Skorzystałem z metody inżynierii wstecznej, aby zidentyfikować odpowiednie zapytania HTTP umożliwiające iterowanie po stronach wyników wyszukiwania serwisu **lubimyczytac.pl**.
    3. Pętla iterowała od strony 1 do 344, zbierając linki do poszczególnych książek.
    4. Z każdego URL-a książki pobierałem szczegóły, takie jak: autor, oceny użytkowników, liczba opinii, kategorie itp.
    5. Dodatkowo, odwiedzałem strony autorów, aby pozyskać dane o nich, takie jak średnia ocena autora, liczba książek, liczba fanów i inne.

    ## Przykład kodu do pozyskiwania danych:
    """)

    st.code("""
import time
import random

import requests
from bs4 import BeautifulSoup
            
from utils.enums import URLS, SOUP

with open(URL_CONFIG_PATH) as url_config_file:
    urls = json.load(url_config_file)

# Initialize lists to store book and author data
books_data_dict_list = []
authors_data_dict_list = []

def scrape_books(base_url, page_url, session):
    #Scrapes book URLs from a given page.
    response = session.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")
    books_urls = [a['href'] for a in soup.find_all('a', class_='book-link')]
    return books_urls

# Starting session
with requests.Session() as session:
    for step in range(1, 344):
        books_urls = scrape_books(base_url=urls[URLS.BASE], page_url=urls[URLS.PAGE].format(step=step), session=session)

        for book_url in books_urls:
            book_html = session.get(book_url).text
            soup_book = BeautifulSoup(book_html, "html.parser")
            authors_html = soup_book.find_all('a', class_='link-name d-inline-block')
            authors_names = [author.text for author in authors_html]
            authors_hrefs = [author['href'] for author in authors_html]
            author_href = authors_hrefs[0]
            author_html = session.get(author_href).text
            author_soup = BeautifulSoup(author_html, "html.parser")
            author_name = author_soup.find('h1').text
            author_rating = float(author_soup.find('span', class_='rating').text.replace(',', '.'))
            author_data_dict = {
                'author_name': author_name,
                'author_rating': author_rating
            }
            authors_data_dict_list.append(author_data_dict)
            book_description = soup_book.find('div', class_='description').text
            book_data_dict = {
                'book_url': book_url,
                'book_description': book_description
            }
            books_data_dict_list.append(book_data_dict)
            time.sleep(random.uniform(0.5, 1.5))

# Display some results
print(f"Scraped {len(books_data_dict_list)} books and {len(authors_data_dict_list)} authors.")
""", language='python')