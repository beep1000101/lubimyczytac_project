from enum import StrEnum

class URLS(StrEnum):
    """
    Enum for URL constants.
    """
    BASE = 'base_url'
    PAGE = 'page_url'

class SOUP(StrEnum):
    """
    Enum for BeautifulSoup parsing constants.
    """
    HTML_PARSER = 'html.parser'
    ANCHOR = 'a'

class BOOKS(StrEnum):
    """
    Enum for book-related CSS classes.
    """
    BOOK_CLASS = 'authorAllBooks__singleTextTitle float-left'
    HREF = 'href'