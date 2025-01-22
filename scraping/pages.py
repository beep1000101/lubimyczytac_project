import requests
from bs4 import BeautifulSoup

from utils.enums import SOUP, BOOKS

def scrape_books(base_url, page_url):
    html = requests.get(page_url).text
    soup_books = BeautifulSoup(html, SOUP.HTML_PARSER)
    books = soup_books.find_all(SOUP.ANCHOR, class_=BOOKS.BOOK_CLASS)
    books_hrefs_suffixes = [book['href'] for book in books]
    books_hrefs = [base_url + suffix for suffix in books_hrefs_suffixes]

    return books_hrefs
    