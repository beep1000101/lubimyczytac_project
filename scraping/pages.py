import requests
from bs4 import BeautifulSoup

from utils.enums import SOUP, BOOKS

def scrape_books(base_url, page_url):
    """
    Scrapes book URLs from a given page URL.

    Parameters
    ----------
    base_url : str
        The base URL of the website.
    page_url : str
        The URL of the page to scrape.

    Returns
    -------
    list
        A list of full URLs to the books found on the page.
    """
    html = requests.get(page_url).text
    soup_books = BeautifulSoup(html, SOUP.HTML_PARSER)
    books = soup_books.find_all(SOUP.ANCHOR, class_=BOOKS.BOOK_CLASS)
    books_hrefs_suffixes = [book['href'] for book in books]
    books_hrefs = [base_url + suffix for suffix in books_hrefs_suffixes]

    return books_hrefs