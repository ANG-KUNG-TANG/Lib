from .user import User, main_database
from .book import Book
import sqlite3

class Admin(User):
    def __init__(self, user_name, password, email, role='admin'):
        super().__init__(user_name, password, email, role)
    
    @staticmethod
    def get_admin_by_id(admin_id):
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ? AND role = ?', (admin_id, 'admin'))
        admin_data = cursor.fetchone()
        conn.close()
        if admin_data:
            return Admin(admin_data[1], admin_data[2], admin_data[3], admin_data[4])
        return None
    
    @staticmethod
    def create_admin(user_name, password, email, role='admin'):
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (user_name, password, email, role) VALUES (?, ?, ?, ?)', 
            (user_name, password, email, role)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def add_book(id, title, author, genre, published_year):
        book = Book(id, title, author, genre, published_year)
        book.save_to_db()

    @staticmethod
    def remove_book(book_id=None, title=None):
        if book_id:
            Book.delete_book_by_id(book_id)
        elif title:
            Book.delete_book_by_title(title)
        else:
            raise ValueError("Either book_id or title must be provided.")

    @staticmethod
    def update_book(book_id, title=None, author=None, genre=None, published_year=None):
        Book.update_book(book_id, title, author, genre, published_year)

    @staticmethod
    def initialize_users_table():
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                role TEXT NOT NULL
            )
            '''
        )
        conn.commit()
        conn.close()
