import sqlite3
import random

main_database = 'books.db'

class Book:
    def __init__(self, title:str, author: str, genre:str, published_year:int,
                 book_id: int = None):
        # Initialize a Book object with given attributes
        self.title = title
        self.author = author
        self.genre = genre
        self.published_year = published_year
        self.book_id = book_id       
            
    def save_to_db(self):
        # Save the book to the database
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()  # Fixed typo here
        # Create the books table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT NOT NULL,
                published_year INTEGER NOT NULL
            )
        ''')
        # Insert the book record
        cursor.execute('''
            INSERT INTO books (book_id, title, author, genre, published_year)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.book_id, self.title, self.author, self.genre, self.published_year))
        conn.commit()
        conn.close()

    @staticmethod
    def get_book_by_id(book_id):
        # Retrieve a book by its ID
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
        book_data = cursor.fetchone()
        conn.close()
        
        if book_data:
            # Return a Book object if found
            return Book(book_data[1], book_data[2], book_data[3], book_data[4], book_data[0])
        return None

    @staticmethod
    def get_book_by_title(title):
        """
        Retrieve all books matching the given title (case-insensitive).
        Returns a list of Book objects.
        """
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE LOWER(title) = LOWER(?)', (title,))
        books_data = cursor.fetchall()
        conn.close()

        return [
            Book(book_data[1], book_data[2], book_data[3], book_data[4], book_data[0])
            for book_data in books_data
        ] if books_data else []

    @staticmethod
    def get_all_books():
        # Retrieve all books from the database
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books')
        books_data = cursor.fetchall()
        conn.close()
        
        # Return list of dicts (JSON-like key-value pairs)
        return [
            {
            "book_id": book_id,
            "title": title,
            "author": author,
            "genre": genre,
            "published_year": published_year
            }
            for book_id, title, author, genre, published_year in books_data
        ]

    @staticmethod
    def delete_book_by_id(book_id):
        # Delete a book by its ID
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE book_id = ?', (book_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_book_by_title(title):
        # Delete a book by its title
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE title = ?', (title,))
        conn.commit()
        conn.close()

    @staticmethod
    def update_book(book_id, title=None, author=None, genre=None, published_year=None):
        # Update book details by its ID
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        # Prepare update fields and parameters
        if title:
            updates.append("title = ?")
            params.append(title)
        if author:
            updates.append("author = ?")
            params.append(author)
        if genre:
            updates.append("genre = ?")
            params.append(genre)
        if published_year:
            updates.append("published_year = ?")
            params.append(published_year)
        
        if updates:
            # Execute the update query if there are fields to update
            query = f"UPDATE books SET {', '.join(updates)} WHERE book_id = ?"
            params.append(book_id)
            cursor.execute(query, tuple(params))
            conn.commit()
        
        conn.close()
        
    def is_available(self):
        """
        Check if this book is available for borrowing.
        Returns True if the book exists in the books table (i.e., not borrowed), else False.
        """
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE book_id = ?', (self.book_id,))
        book = cursor.fetchone()
        conn.close()
        return book is not None

    @staticmethod
    def get_available_books():
        """
        Retrieve all books that are currently available (i.e., present in the books table).
        Returns a list of dicts.
        """
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books')
        books_data = cursor.fetchall()
        conn.close()
        return [
            {
                "book_id": book_id,
                "title": title,
                "author": author,
                "genre": genre,
                "published_year": published_year
            }
            for book_id, title, author, genre, published_year in books_data
        ]
    
    @staticmethod
    def borrow_book(book_id, user_id):
        """
        Borrow a book by its ID for a user.
        Deducts the book from available inventory and marks it as borrowed by the user.
        """
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()

        # Check if the book exists and is available
        cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
        book = cursor.fetchone()
        if not book:
            conn.close()
            raise ValueError("Book not found.")

        # Check if the user exists
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            raise ValueError("User not found.")

        # Check if the user already borrowed this book
        borrowed_books = user[5] if user[5] else ""
        borrowed_list = borrowed_books.split(',') if borrowed_books else []
        if str(book_id) in borrowed_list:
            conn.close()
            raise ValueError("Book already borrowed by this user.")

        # Remove the book from the books table (deduct from inventory)
        cursor.execute('DELETE FROM books WHERE book_id = ?', (book_id,))

        # Update user's borrowed_books
        borrowed_list.append(str(book_id))
        updated_borrowed_books = ','.join(borrowed_list)
        cursor.execute('UPDATE users SET borrowed_books = ? WHERE id = ?', (updated_borrowed_books, user_id))

        conn.commit()
        conn.close()
        
    @staticmethod
    def initialize_books_table():
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT NOT NULL,
                published_year INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        
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
                role TEXT NOT NULL,
                borrowed_books TEXT
            )
            '''
        )
        conn.commit()
        conn.close()
        
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE users ADD COLUMN borrowed_books TEXT;")
        conn.commit()
        conn.close()
        