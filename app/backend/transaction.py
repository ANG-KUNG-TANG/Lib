import datetime
from app.backend.user import User
from app.backend.book import Book

class Transaction:
    def __init__(self, user: User):
        self.user = user
        self.transactions = []

    def borrow_book(self, book_id):
        """Borrow a book by its ID for the user."""
        book = Book.get_book_by_id(book_id)
        if book and book.is_available():
            book.borrow_book(self.user.user_id)
            transaction = {
                'book_id': book_id,
                'user_id': self.user.user_id,
                'borrowed_at': datetime.datetime.now()
            }
            self.transactions.append(transaction)
            return transaction
        return None

    def return_book(self, book_id):
        """Return a book by its ID for the user."""
        book = Book.get_book_by_id(book_id)
        if book:
            book.return_book(self.user.user_id)
            transaction = {
                'book_id': book_id,
                'user_id': self.user.user_id,
                'returned_at': datetime.datetime.now()
            }
            self.transactions.append(transaction)
            return transaction
        return None
