import re
from datetime import date

# Założenia walidacji danych wejściowych dla książki:
#  - name:   1-64 znaki; litery (także polskie), cyfry, spacja oraz . , : ; ! ? ' ( ) -
#  - author: 1-64 znaki; litery (także polskie), spacja oraz . ' -
#  - year_published: liczba całkowita od 1 do bieżącego roku
#  - book_type: tylko jedna z wartości 2days, 5days, 10days
# Znaki < > " & / = ` nie są dozwolone, więc nie da się wstrzyknąć kodu HTML/JavaScript.

MAX_TEXT_LENGTH = 64
NAME_PATTERN = re.compile(r"^[A-Za-z0-9ĄĆĘŁŃÓŚŹŻąćęłńóśźż .,:;!?'()\-]+$")
AUTHOR_PATTERN = re.compile(r"^[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż .'\-]+$")
ALLOWED_BOOK_TYPES = {"2days", "5days", "10days"}


def _validate_text(value, field, pattern):
    if not isinstance(value, str):
        raise ValueError(f"{field}: wartość musi być tekstem")
    value = value.strip()  # normalizacja przed walidacją - zapisujemy to, co sprawdziliśmy
    if not 1 <= len(value) <= MAX_TEXT_LENGTH:  # rozmiar
        raise ValueError(f"{field}: długość musi wynosić od 1 do {MAX_TEXT_LENGTH} znaków")
    if not pattern.fullmatch(value):  # dozwolone znaki
        raise ValueError(f"{field}: zawiera niedozwolone znaki")
    return value


def validate_name(value):
    return _validate_text(value, "name", NAME_PATTERN)


def validate_author(value):
    return _validate_text(value, "author", AUTHOR_PATTERN)


def validate_year_published(value):
    if isinstance(value, bool):
        raise ValueError("year_published: wartość musi być liczbą całkowitą")
    try:
        year = int(str(value).strip())
    except (TypeError, ValueError):
        raise ValueError("year_published: wartość musi być liczbą całkowitą")
    if not 1 <= year <= date.today().year:
        raise ValueError(f"year_published: rok musi być z zakresu 1-{date.today().year}")
    return year


def validate_book_type(value):
    if value not in ALLOWED_BOOK_TYPES:
        raise ValueError(f"book_type: dozwolone wartości to {', '.join(sorted(ALLOWED_BOOK_TYPES))}")
    return value
