from sqlalchemy import and_

from sqlalchemy.orm import sessionmaker
from connection import engine
from models import Books, Authors, Genres, Readers, BorrowedBooks
from datetime import datetime

# ############## Управление книгами:

Session = sessionmaker(bind=engine)


# Изменение книги
def update_book(_book, _updated_data):
    with Session(autoflush=False, bind=engine) as db:
        for key, value in _updated_data.items():
            setattr(_book, key, value)
        db.commit()
        return _book


# Удаление книги
def delete_book(_book):
    with Session(autoflush=False, bind=engine) as db:
        db.delete(_book)
        db.commit()


# Добавить автора для книги
def add_author_to_book(_book, _author_id):
    with Session(autoflush=False, bind=engine) as db:
        author = db.query(Authors).get(_author_id)
        if author:
            _book.authors.append(author)
            db.commit()


# Удалить автора для книги
def remove_author_from_book(_book, _author_id):
    with Session(autoflush=False, bind=engine) as db:
        author = db.query(Authors).get(_author_id)
        if author in _book.authors:
            _book.authors.remove(author)
            db.commit()


# Добавить жанр книги
def add_genre_to_book(_book, _genre_id):
    with Session(autoflush=False, bind=engine) as db:
        genre = db.query(Genres).get(_genre_id)
        if genre:
            _book.genres.append(genre)
            db.commit()


# Удалить жанр книги
def remove_genre_from_book(_book, _genre_id):
    with Session(autoflush=False, bind=engine) as db:
        genre = db.query(Genres).get(_genre_id)
        if genre in _book.genres:
            _book.genres.remove(genre)
            db.commit()


# ############## Управление читателями:
# Показать читателей
def get_reader(reader_id: int):
    with Session(autoflush=False, bind=engine) as db:
        return db.query(Readers).get(reader_id)


# Создать читателя
def create_reader(reader_data: dict):
    with Session(autoflush=False, bind=engine) as db:
        reader = Readers(**reader_data)
        db.add(reader)
        db.commit()
        db.refresh(reader)
        return reader


# Измененить читателя
def update_reader(reader: Readers, updated_data: dict):
    with Session(autoflush=False, bind=engine) as db:
        for key, value in updated_data.items():
            setattr(reader, key, value)
        db.commit()
        return reader


# Удалить читателя
def delete_reader(reader: Readers):
    with Session(autoflush=False, bind=engine) as db:
        db.delete(reader)
        db.commit()


# ======================================= РАБОТАЕТ ==================================

# Создание новой книги
def create_book(_book_data):
    with Session(autoflush=False, bind=engine) as db:
        book = Books(**_book_data)
        db.add(book)
        db.commit()
        if book:
            return "Книга создана!!!"
        else:
            return False


# Получение всего списка книг
def get_book_all():
    with Session(autoflush=False, bind=engine) as db:
        book_seek = db.query(Books).distinct().all()
        if book_seek:
            books_data = []
            for book in book_seek:
                book_data = {
                    'id': book.id,
                    'title': book.title,
                    'publication': book.publication,
                    'publication_date': book.publication_date,
                    'cover_image': book.cover_image,
                    'book_location': book.book_location,
                    'description': book.description,
                    'price': book.price,
                    'available_copies': book.available_copies
                }
                books_data.append(book_data)
            return books_data
        else:
            return None


# Поиск книги по id
def get_book(_book_id):
    with Session(autoflush=False, bind=engine) as db:
        book_seek = db.query(Books).filter_by(id=_book_id).first()
        if book_seek:
            book_data = {
                'id': book_seek.id,
                'title': book_seek.title,
                'publication': book_seek.publication,
                'publication_date': book_seek.publication_date,
                'cover_image': book_seek.cover_image,
                'book_location': book_seek.book_location,
                'description': book_seek.description,
                'price': book_seek.price,
                'available_copies': book_seek.available_copies
            }
            return book_data
        else:
            return None


# Поиск активностей конкретного читателя
def get_reader_activity(_reader_id):
    with Session(autoflush=False, bind=engine) as db:
        reader = db.query(Readers).get(_reader_id)
        if not reader:
            return None, 404
        borrowed_books = (
            db.query(BorrowedBooks)
            .join(Books)
            .filter(BorrowedBooks.reader_id == _reader_id)
            .all()
        )
        activity = []
        for borrowed_book in borrowed_books:
            book = borrowed_book.book
            activity.append({
                "book": book,
                "date_borrowed": borrowed_book.date_borrowed,
                "date_returned": borrowed_book.date_returned,
                "is_returned": borrowed_book.is_returned
            })
        return activity, 200
