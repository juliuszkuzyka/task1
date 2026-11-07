import unittest
from datetime import date

from project.books.models import Book
from project.books.validators import (validate_name, validate_author,
                                      validate_year_published, validate_book_type)

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "\"><script>alert(1)</script>",
    "javascript:alert(1)//<a>",
]


class TestValidatorsValid(unittest.TestCase):
    """Poprawne dane muszą zostać przyjęte."""

    def test_valid_name(self):
        self.assertEqual(validate_name("Pan Tadeusz"), "Pan Tadeusz")
        self.assertEqual(validate_name("Harry Potter (tom 1): Kamień Filozoficzny"),
                         "Harry Potter (tom 1): Kamień Filozoficzny")

    def test_valid_name_is_stripped(self):
        self.assertEqual(validate_name("  Lalka  "), "Lalka")

    def test_valid_author(self):
        self.assertEqual(validate_author("Adam Mickiewicz"), "Adam Mickiewicz")
        self.assertEqual(validate_author("J.R.R. Tolkien"), "J.R.R. Tolkien")
        self.assertEqual(validate_author("Flannery O'Connor"), "Flannery O'Connor")

    def test_valid_year(self):
        self.assertEqual(validate_year_published("1834"), 1834)
        self.assertEqual(validate_year_published(date.today().year), date.today().year)

    def test_valid_book_type(self):
        for book_type in ("2days", "5days", "10days"):
            self.assertEqual(validate_book_type(book_type), book_type)


class TestValidatorsInvalid(unittest.TestCase):
    """Niepoprawne dane, w tym próby XSS, muszą zostać odrzucone."""

    def test_xss_in_name_rejected(self):
        for payload in XSS_PAYLOADS:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    validate_name(payload)

    def test_xss_in_author_rejected(self):
        for payload in XSS_PAYLOADS:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    validate_author(payload)

    def test_empty_and_too_long_rejected(self):
        for value in ("", "   ", "a" * 65):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_name(value)
                with self.assertRaises(ValueError):
                    validate_author(value)

    def test_non_string_rejected(self):
        with self.assertRaises(ValueError):
            validate_name(None)
        with self.assertRaises(ValueError):
            validate_author(123)

    def test_invalid_year_rejected(self):
        for value in ("abc", "", None, 0, -5, date.today().year + 1, True):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_year_published(value)

    def test_invalid_book_type_rejected(self):
        for value in ("", "1day", "<script>alert(1)</script>", None):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_book_type(value)


class TestBookModel(unittest.TestCase):
    """Walidacja działa na poziomie tworzenia i edycji obiektu Book."""

    def test_create_valid_book(self):
        book = Book(name="Lalka", author="Bolesław Prus", year_published="1890", book_type="5days")
        self.assertEqual(book.name, "Lalka")
        self.assertEqual(book.year_published, 1890)

    def test_create_book_with_xss_rejected(self):
        with self.assertRaises(ValueError):
            Book(name="<script>alert('XSS')</script>", author="Autor", year_published=2000, book_type="2days")
        with self.assertRaises(ValueError):
            Book(name="Lalka", author="<img src=x onerror=alert(1)>", year_published=2000, book_type="2days")

    def test_edit_book_with_xss_rejected(self):
        book = Book(name="Lalka", author="Bolesław Prus", year_published=1890, book_type="5days")
        with self.assertRaises(ValueError):
            book.name = "<script>alert('XSS')</script>"
        self.assertEqual(book.name, "Lalka")


if __name__ == "__main__":
    unittest.main()
