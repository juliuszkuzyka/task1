import unittest
from datetime import datetime

from project.customers.models import Customer
from project.customers.validators import validate_customer_name, validate_city, validate_age
from project.loans.models import Loan

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "\"><script>alert(1)</script>",
]


class TestCustomerValidatorsValid(unittest.TestCase):
    """Poprawne dane klienta muszą zostać przyjęte."""

    def test_valid_name(self):
        self.assertEqual(validate_customer_name("Jan Kowalski"), "Jan Kowalski")
        self.assertEqual(validate_customer_name("Anna Nowak-Wiśniewska"), "Anna Nowak-Wiśniewska")
        self.assertEqual(validate_customer_name("  Łukasz Żak  "), "Łukasz Żak")

    def test_valid_city(self):
        self.assertEqual(validate_city("Warszawa"), "Warszawa")
        self.assertEqual(validate_city("Bielsko-Biała"), "Bielsko-Biała")

    def test_valid_age(self):
        self.assertEqual(validate_age("25"), 25)
        self.assertEqual(validate_age(0), 0)
        self.assertEqual(validate_age(150), 150)


class TestCustomerValidatorsInvalid(unittest.TestCase):
    """Niepoprawne dane klienta, w tym próby XSS, muszą zostać odrzucone."""

    def test_xss_in_name_rejected(self):
        for payload in XSS_PAYLOADS:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    validate_customer_name(payload)

    def test_xss_in_city_rejected(self):
        for payload in XSS_PAYLOADS:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    validate_city(payload)

    def test_empty_and_too_long_rejected(self):
        for value in ("", "   ", "a" * 65):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_customer_name(value)
                with self.assertRaises(ValueError):
                    validate_city(value)

    def test_invalid_age_rejected(self):
        for value in ("abc", "", None, -1, 151, True):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_age(value)


class TestCustomerModel(unittest.TestCase):
    """Walidacja działa przy tworzeniu i edycji obiektu Customer."""

    def test_create_valid_customer(self):
        customer = Customer(name="Jan Kowalski", city="Kraków", age="30")
        self.assertEqual(customer.name, "Jan Kowalski")
        self.assertEqual(customer.age, 30)

    def test_create_customer_with_xss_rejected(self):
        with self.assertRaises(ValueError):
            Customer(name="<script>alert('XSS')</script>", city="Kraków", age=30)
        with self.assertRaises(ValueError):
            Customer(name="Jan Kowalski", city="<img src=x onerror=alert(1)>", age=30)

    def test_edit_customer_with_xss_rejected(self):
        customer = Customer(name="Jan Kowalski", city="Kraków", age=30)
        with self.assertRaises(ValueError):
            customer.city = "<script>alert('XSS')</script>"
        self.assertEqual(customer.city, "Kraków")


class TestLoanModel(unittest.TestCase):
    """Wypożyczenie przyjmuje tylko poprawne nazwy klienta i książki."""

    def _loan(self, customer_name="Jan Kowalski", book_name="Lalka"):
        return Loan(customer_name=customer_name, book_name=book_name,
                    loan_date=datetime(2026, 11, 1), return_date=datetime(2026, 11, 10),
                    original_author="Bolesław Prus", original_year_published=1890,
                    original_book_type="5days")

    def test_create_valid_loan(self):
        loan = self._loan()
        self.assertEqual(loan.customer_name, "Jan Kowalski")
        self.assertEqual(loan.book_name, "Lalka")

    def test_create_loan_with_xss_rejected(self):
        for payload in XSS_PAYLOADS:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    self._loan(customer_name=payload)
                with self.assertRaises(ValueError):
                    self._loan(book_name=payload)


if __name__ == "__main__":
    unittest.main()
