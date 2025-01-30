import streamlit as st


def show_data_acquisition():
    st.title("Pozyskiwanie danych")

    st.markdown("""
    ## Jak pozyskiwałem dane?

    Aby zebrać dane, wykorzystałem język Python oraz dwie popularne biblioteki: **requests** oraz **BeautifulSoup**.

    1. **requests** pozwala na wysyłanie zapytań HTTP do strony, a **BeautifulSoup** ułatwia parsowanie HTML.
    2. Skorzystałem z metody inżynierii wstecznej, aby zidentyfikować odpowiednie zapytania HTTP umożliwiające iterowanie po stronach wyników wyszukiwania serwisu **lubimyczytac.pl**.
    3. Pętla iterowała od strony 1 do 344, zbierając linki do poszczególnych książek.
    4. Z każdego URL-a książki pobierałem szczegóły, takie jak: autor, oceny użytkowników, liczba opinii, kategorie itp.
    5. Dodatkowo, odwiedzałem strony autorów, aby pozyskać dane o nich, takie jak średnia ocena autora, liczba książek, liczba fanów i inne.

    ## Skrypt do pozyskiwania danych:
    """)

    st.code("""
import json
import re
import time
import random

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

from utils.paths import URL_CONFIG_PATH, BOOKS_PATH, AUTHORS_PATH
from utils.enums import URLS, SOUP
from utils.regex import NUMBER_PATTERN, LITERAL_PATTERN

from scraping.pages import scrape_books
from scraping.session import get_session
            
with open(URL_CONFIG_PATH) as url_config_file:
    urls = json.load(url_config_file)

def get_with_retry(session, url, retries=5):
    for _ in range(retries):
        try:
            html = session.get(url).text
            break
        except Exception as e:
            print(f'Error: {e}')
            time.sleep(.5)
    return html

session = get_session()

# Main data sourcing part of the script            

# Initialize lists to store book and author data
books_data_dict_list = []
authors_data_dict_list = []

# give visited_books
if BOOKS_PATH.exists():
    visited_books = set(pd.read_csv(BOOKS_PATH)['url'].unique())
else:
    visited_books = set()

# give visited_authors
if AUTHORS_PATH.exists():
    visited_authors = set(pd.read_csv(AUTHORS_PATH)['author_url'].unique())
else:
    visited_authors = set()

# Loop through pages to scrape book URLs
try:
    for step in range(1, 344):
        books_urls = scrape_books(base_url=urls[URLS.BASE], page_url=urls[URLS.PAGE].format(step=step), session=session)
        # books_urls = scrape_books(base_url=urls[URLS.BASE], page_url=urls['page_url_additional'].format(step=step), session=session)
        
        # Loop through each book URL to scrape book details
        for book_url in books_urls:
            # book_html = session.get(book_url).text
            book_html = get_with_retry(session, book_url)
            soup_book = BeautifulSoup(book_html, SOUP.HTML_PARSER)
            

            # Extract author names and hrefs
            authors_html = soup_book.find_all('a', class_='link-name d-inline-block')
            authors_names = [author.text for author in authors_html]
            authors_hrefs = [author['href'] for author in authors_html]

            # Scrape author
            author_href = authors_hrefs[0]
            if author_href not in visited_authors:
                author_html = get_with_retry(session, author_href)
                author_soup = BeautifulSoup(author_html, SOUP.HTML_PARSER)
                author_author_name = author_soup.find('div', class_='author-main__header-wrapper').text
                author_average_rating = float(author_soup.find('div', class_='author-box').find('span', class_='rating__avarage').text.replace(',', '.'))
                readers_div = author_soup.find_all('div', class_='author-box__readers-col')
                if readers_div is not None:
                    author_number_of_people_read = int(readers_div[0].find('span').text.replace(' ', ''))
                    number_of_people_wants_to_read = int(readers_div[1].find('span').text.replace(' ', ''))
                else:
                    author_number_of_people_read = float('nan')
                    number_of_people_wants_to_read = float('nan')
                author_date_of_birth_span = author_soup.find('span', class_='author-info__born')
                if author_date_of_birth_span is not None:
                    author_date_of_birth =  author_date_of_birth_span.text.split()[-1]
                else:
                    author_date_of_birth = 'Unknown'
                author_number_of_fans = int(author_soup.find('span', class_='author-box__number').text.replace(' ', ''))
                author_number_of_books_written = int(author_soup.find('div', class_='author-info__count').text)
                author_awards_html = author_soup.find('div', class_='author-info__count author-info__count--awards')
                if author_awards_html is not None:
                    author_number_of_awards = int(author_awards_html.text)
                else:
                    author_number_of_awards = 0
                author_data_dict = {
                    'author_name': author_author_name,
                    'author_url': author_href,
                    'author_average_rating': author_average_rating,
                    'author_number_of_people_read': author_number_of_people_read,
                    'author_number_of_people_wants_to_read': number_of_people_wants_to_read,
                    'author_date_of_birth': author_date_of_birth,
                    'author_number_of_fans': author_number_of_fans,
                    'author_number_of_books_written': author_number_of_books_written,
                    'author_number_of_awards': author_number_of_awards
                }
                authors_data_dict_list.append(author_data_dict)
                visited_authors.add(author_href)
            # Scrape author end

            # scrape publisher
            ...
            # scrape publisher end
            if book_url in visited_books:
                continue
            # Create a dictionary for authors
            authors = {}
            for index, (author_name, author_href) in enumerate(zip(authors_names, authors_hrefs)):
                number = index if index > 0 else ''
                authors[f'author{number}'] = author_name
                authors[f'author_href{number}'] = author_href
            
            # Extract book details
            pages_html = soup_book.find('span', class_='d-sm-inline-block book-pages book__pages pr-2 mr-2 pr-sm-3 mr-sm-3')
            description_html = soup_book.find('div', class_='collapse-content')
            description = description_html.text if description_html else ''
            
            # Extract user statistics
            user_stats_html = soup_book.find('div', class_='d-flex flex-wrap justify-content-around px-3')
            if user_stats_html is None:
                number_of_discussions = 0
                number_of_user_opinions = 0
                number_of_user_ratings = 0
            else:
                user_stats = user_stats_html.text
                user_stats = list(map(int, re.findall(NUMBER_PATTERN, user_stats)))
            
                if len(user_stats) == 2:
                    number_of_user_opinions, number_of_user_ratings = user_stats
                    number_of_discussions = 0
                elif len(user_stats) == 3:
                    number_of_user_opinions, number_of_user_ratings, number_of_discussions = user_stats
            
            # Extract additional book details
            details_dict = dict(zip(
                [element.text.strip().rstrip(':') for element in soup_book.find_all('dt')],
                [element.text.strip() for element in soup_book.find_all('dd')]
            ))
            
            # Extract on-the-shelf statistics
            on_the_shelf_dict_raw = {
                re.search(LITERAL_PATTERN, element.text).group().strip(): "".join(re.findall(NUMBER_PATTERN, element.text))
                for element in soup_book.find_all('li', class_='list-group-item p-0')
            }
            on_the_shelf_dict = {
                'number_of_people_read': on_the_shelf_dict_raw.get('Przeczytane', np.nan),
                'number_of_people_has': on_the_shelf_dict_raw.get('Posiadam', np.nan),
                'number_of_people_favorite': on_the_shelf_dict_raw.get('Ulubione', np.nan),
                'number_of_people_wants_to_read': on_the_shelf_dict_raw.get('Chcę przeczytać', np.nan),
                'number_of_people_wants_as_gift': on_the_shelf_dict_raw.get('Chcę w prezencie', np.nan),
                'number_of_people_currently_read': on_the_shelf_dict_raw.get('Teraz czytam', np.nan)
            }
            
            # Extract tags
            tags = '&'.join([element.text.strip() for element in soup_book.find_all('a', class_='tag')])
            
            # Extract ratings
            ratings_dict = {
                f'rating_{element["data-rating"]}': int("".join(re.findall(NUMBER_PATTERN, element.text.strip())))
                for element in soup_book.find_all('a', class_='chart-valuebtn btn-link--without-bold plusCountModal')
            }
            
            # Combine all extracted data into a single dictionary
            books_data_dict = {
                **authors,
                'description': description,
                'number_of_user_opinions': number_of_user_opinions,
                'number_of_user_ratings': number_of_user_ratings,
                'number_of_discussions': number_of_discussions,
                **details_dict,
                **on_the_shelf_dict,
                'tags': tags,
                **ratings_dict,
                'url': book_url
            }
            
            # Append the book data dictionary to the list
            books_data_dict_list.append(books_data_dict)
            
            # Sleep for a random time between requests to avoid being blocked
            # random_sleep_time = random.uniform(0.5, 1.5)
            random_sleep_time = random.uniform(0.3, 0.8)
            time.sleep(random_sleep_time)
        # print current step of the loop and the only current step of the loop
        print(f'Current step: {step}', end='\r')
except Exception as e:
    print(f'Error: {e}')
    # print traceback
    import traceback
    print('something went wrong')
    traceback.print_exc()
    # save data frames as tmp data frames to be merged later
    books_df_tmp = pd.DataFrame(books_data_dict_list)
    authors_df_tmp = pd.DataFrame(authors_data_dict_list)
    books_df_tmp.to_csv('books_tmp1.csv', index=False)
    authors_df_tmp.to_csv('authors_tmp1.csv', index=False)
    print('tmp data frames saved')

""", language='python')