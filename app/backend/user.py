import random
import sqlite3

main_database = 'users.db'

class User:
    @staticmethod
    def generate_user_id():
        # Generates a 6-digit user ID as a string
        return f"{random.randint(100000, 999999)}"
    
    def __init__(self, user_name, password, email, role='user', user_id=None):
        self.id = user_id if user_id is not None else self.generate_user_id()
        self.user_name = user_name
        self.password = password
        self.email = email
        self.role = role
        self.borrowed_books = []  # Add this line
    
    def borrow_book(self, book):
        # Logic for borrowing a book (placeholder)
        print(f"{self.user_name} borrowed {book.title}")

    def return_book(self, book):
        # Logic for returning a book (placeholder)
        print(f"{self.user_name} returned {book.title}")
        
    def save_to_db(self):
        # Save the user to the database, creating the table if it doesn't exist
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_name TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL,
                borrowed_books TEXT
            )
        ''')
        cursor.execute('''
            INSERT INTO users (id, user_name, password, email, role, id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.id, self.user_name, self.password, self.email, self.role, self.generate_user_id()))
        conn.commit()
        conn.close()
        
    @staticmethod
    def get_user_by_id(user_id):
        # Retrieve a user from the database by their ID
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return User(user_data[1], user_data[2], user_data[3], user_data[4])
        return None
    @staticmethod
    def create_user(user_name, password, email, role='member'):
        # Create a new user and save to the database
        user = User(user_name, password, email, role)
        user.save_to_db()
        return user

    @staticmethod
    def get_user_by_username(user_name):
        # Retrieve a user from the database by their username
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_name = ?', (user_name,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return User(user_data[1], user_data[2], user_data[3], user_data[4])
        return None
    
    @staticmethod
    def get_all_users():
        # Retrieve all users from the database
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users_data = cursor.fetchall()
        conn.close()
        
        users = []
        for user_data in users_data:
            users.append(User(user_data[1], user_data[2], user_data[3], user_data[4]))
        return users
    
    @staticmethod
    def delete_user(user_id):
        # Delete a user from the database by their ID
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def update_user(user_id, user_name=None, password=None, email=None, role=None):
        # Update user details in the database
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        
        if user_name:
            cursor.execute('UPDATE users SET user_name = ? WHERE id = ?', (user_name, user_id))
        if password:
            cursor.execute('UPDATE users SET password = ? WHERE id = ?', (password, user_id))
        if email:
            cursor.execute('UPDATE users SET email = ? WHERE id = ?', (email, user_id))
        if role:
            cursor.execute('UPDATE users SET role = ? WHERE id = ?', (role, user_id))
        
        conn.commit()
        conn.close()
        
    @staticmethod
    def authenticate(user_name, password):
        # Authenticate a user by username and password
        user = User.get_user_by_username(user_name)
        if user and user.password == password:
            return user
        return None

    @staticmethod
    def get_user_by_email(email):
        # Retrieve a user from the database by their email
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return User(user_data[1], user_data[2], user_data[3], user_data[4])
        return None
    
    @staticmethod
    def get_user_by_role(role):
        # Retrieve all users with a specific role
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE role = ?', (role,))
        users_data = cursor.fetchall()
        conn.close()
        
        users = []
        for user_data in users_data:
            users.append(User(user_data[1], user_data[2], user_data[3], user_data[4]))
        return users

    @staticmethod
    def get_user_by_id_and_role(user_id, role):
        # Retrieve a user by both ID and role
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ? AND role = ?', (user_id, role))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return User(user_data[1], user_data[2], user_data[3], user_data[4])
        return None

    @staticmethod
    def validate_email(email):
        # Validate email format using regex
        import re
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def validate_password(password):
        # Validate password (at least 8 chars, at least one letter and one number)
        import re
        password_regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
        return re.match(password_regex, password) is not None

    @staticmethod
    def validate_username(username):
        # Validate username (at least 3 chars, only letters, numbers, underscores)
        import re
        username_regex = r'^[a-zA-Z0-9_]{3,}$'
        return re.match(username_regex, username) is not None

    @staticmethod
    def to_dict(user):
        # Convert user object to JSON-like dictionary
        return {
            'id': user.id,
            'user_name': user.user_name,
            'email': user.email,
            'role': user.role,
            'borrowed_books': user.borrowed_books  # Assuming borrowed_books is a list
        }
    @staticmethod
    def log(message):
        # Log a message to the console
        print(f"[LOG] {message}")

    @staticmethod
    def error(message):
        # Log an error message to the console
        print(f"[ERROR] {message}")
    @staticmethod
    def login_user(user_id, password):
        # Authenticate a user and return their details
        user = User.authenticate(user_id, password)        
    @staticmethod
    def user_profile(user_name):
        """
        Retrieve user profile details by user ID.
        """
        user = User.get_user_by_id(user_id=user_name)
        if user:
            return {
                'id': user.id,
                'user_name': user.user_name,
                'email': user.email,
                'role': user.role,
                'borrowed_books': []  # Placeholder for borrowed books
            }
        else:
            User.error(f"User with ID {user_name} not found.")
            return None
    @staticmethod
    def get_all_users_with_borrowed_books():
        conn = sqlite3.connect(main_database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_name, email, borrowed_books FROM users WHERE borrowed_books IS NOT NULL AND borrowed_books != ''")
        users = cursor.fetchall()
        conn.close()
        return users

# Database migration code


conn = sqlite3.connect(main_database)
cursor = conn.cursor()
try:
    cursor.execute("ALTER TABLE users ADD COLUMN borrowed_books TEXT;")
    print("Column 'borrowed_books' added.")
except sqlite3.OperationalError:
    print("Column 'borrowed_books' already exists.")
conn.commit()
conn.close()