import re

# Założenia walidacji danych wejściowych dla klienta:
#  - name: 1-64 znaki; litery (także polskie), spacja oraz . ' -
#  - city: 1-64 znaki; litery (także polskie), spacja oraz -
#  - age:  liczba całkowita od 0 do 150
# Znaki < > " & / = ` nie są dozwolone, więc nie da się wstrzyknąć kodu HTML/JavaScript.

MAX_TEXT_LENGTH = 64
NAME_PATTERN = re.compile(r"^[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż .'\-]+$")
CITY_PATTERN = re.compile(r"^[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż \-]+$")


def _validate_text(value, field, pattern):
    if not isinstance(value, str):
        raise ValueError(f"{field}: wartość musi być tekstem")
    value = value.strip()  # normalizacja przed walidacją - zapisujemy to, co sprawdziliśmy
    if not 1 <= len(value) <= MAX_TEXT_LENGTH:  # rozmiar
        raise ValueError(f"{field}: długość musi wynosić od 1 do {MAX_TEXT_LENGTH} znaków")
    if not pattern.fullmatch(value):  # dozwolone znaki
        raise ValueError(f"{field}: zawiera niedozwolone znaki")
    return value


def validate_customer_name(value):
    return _validate_text(value, "name", NAME_PATTERN)


def validate_city(value):
    return _validate_text(value, "city", CITY_PATTERN)


def validate_age(value):
    if isinstance(value, bool):
        raise ValueError("age: wartość musi być liczbą całkowitą")
    try:
        age = int(str(value).strip())
    except (TypeError, ValueError):
        raise ValueError("age: wartość musi być liczbą całkowitą")
    if not 0 <= age <= 150:
        raise ValueError("age: wiek musi być z zakresu 0-150")
    return age
