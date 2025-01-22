from enum import StrEnum

class URLS(StrEnum):
    BASE = 'base_url'
    PAGE = 'page_url'

class SOUP(StrEnum):
    HTML_PARSER = 'html.parser'
    ANCHOR = 'a'

class BOOKS(StrEnum):
    BOOK_CLASS = 'authorAllBooks__singleTextTitle float-left'
    