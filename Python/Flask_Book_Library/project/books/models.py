from sqlalchemy.orm import validates
from project import db, app
from project.books.validators import (validate_name, validate_author,
                                      validate_year_published, validate_book_type)


# Book model
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    author = db.Column(db.String(64))
    year_published = db.Column(db.Integer) 
    book_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default='available')

    def __init__(self, name, author, year_published, book_type, status='available'):
        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.status = status

    # Walidacja na poziomie modelu: @validates uruchamia się przy każdym przypisaniu
    # pola, czyli zarówno w __init__ (tworzenie), jak i przy edycji książki.
    # Niepoprawnego obiektu Book nie da się utworzyć ani zapisać.
    @validates('name')
    def _validate_name(self, key, value):
        return validate_name(value)

    @validates('author')
    def _validate_author(self, key, value):
        return validate_author(value)

    @validates('year_published')
    def _validate_year_published(self, key, value):
        return validate_year_published(value)

    @validates('book_type')
    def _validate_book_type(self, key, value):
        return validate_book_type(value)

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()