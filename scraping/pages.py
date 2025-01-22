import requests
from bs4 import BeautifulSoup

from utils.enums import SOUP, BOOKS

def scrape_books(url):
    html = requests.get(url).text
    soup_books = BeautifulSoup(html, SOUP.HTML_PARSER)
    books = soup_books.find_all(SOUP.ANCHOR), class_=BOOKS.BOOK_CLASS)
    books_hrefs = [book['href'] for book in books]

    return books_hrefs
    