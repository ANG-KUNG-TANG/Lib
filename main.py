from app.backend.user import User, main_database
from app.backend.admin import Admin
from app.backend.book import Book, main_database
from app.backend.transaction import Transaction
import sqlite3


def main():
    print('Welcome to the Library')
    # Ensure users table exists before any operation
    Admin.initialize_users_table()
    while True:
        option = input("Choose an option\n 1. Register\n 2. Login\n 3. Exit\n Option: ")
        if option == '1':
            user_name = input("Enter your username: ")
            password = input("Enter your password: ")
            email = input("Enter your email: ")
            role = input("Enter your role (user/admin): ").lower()
            user_id = User.generate_user_id()
            print(f"Your User ID is: {user_id}")

            if role not in ['user', 'admin']:
                print("Invalid role. Please choose 'user' or 'admin'.")
                continue

            if role == 'admin':
                Admin.create_admin(user_name, password, email, role)
            else:
                User.create_user(user_name, password, email, role)

            print(f"{role.capitalize()} registered successfully!")

        elif option == '2':
            try:
                print("Login to your account")
                login_role = input("1.Admin 2.User\n Choose role: ")
                if login_role not in ['1', '2']:
                    print("Invalid option. Please choose 1 or 2.")
                    continue
                user_id = input("Enter User ID: ")
                password = input("Enter Password: ")
                role = 'admin' if login_role == '1' else 'user'
                user = login_user(user_id, password, role)
                if user:
                    print(f"Login successful for {user['name']}.")
                    print("Profile:", user)
                    if user['role'] == 'admin':
                        # Admin menu
                        while True:
                            print("\nAdmin Menu:")
                            print("1. Add Book")
                            print("2. Update Book")
                            print("3. View Book by Title")
                            print("4. List All Available Books")
                            print('5. View borrowed books')
                            print("6. Logout")
                            admin_action = input("Choose an option: ")
                            if admin_action == '1':
                                # Add Book
                                try:
                                    book_id = input('Enter Book ID : ')
                                    title = input("Title: ")
                                    author = input("Author: ")
                                    genre = input("Genre: ")
                                    published_year = input("Published Year: ")
                                    Admin.add_book(book_id, title, author, genre, published_year)
                                    print("Book added successfully.")
                                except Exception as e:
                                    print("Error adding book:", e)
                            elif admin_action == '2':
                                # Update Book
                                book_id = input("Enter Book ID to update: ")
                                title = input("New Title (leave blank to skip): ")
                                author = input("New Author (leave blank to skip): ")
                                genre = input("New Genre (leave blank to skip): ")
                                published_year = input("New Published Year (leave blank to skip): ")
                                Admin.update_book(
                                    book_id,
                                    title if title else None,
                                    author if author else None,
                                    genre if genre else None,
                                    published_year if published_year else None
                                )
                                print("Book info updated successfully.")
                            elif admin_action == '3':
                                # View Book by Title
                                book_title = input("Enter the title of the book to view: ")
                                if not book_title.strip():
                                    print("Book title cannot be empty.")
                                    continue
                                found_books = Book.get_book_by_title(book_title)
                                if found_books:
                                    print("Book Info:")
                                    print(found_books[0])
                                else:
                                    print("Book not found.")
                            elif admin_action == '4':
                                # List all available books
                                available_books = Book.get_all_books()
                                if available_books:
                                    print("Available Books:")
                                    for book in available_books:
                                        if isinstance(book, dict):
                                            print(f"ID: {book.get('book_id')}, Title: {book.get('title')}\n, Author: {book.get('author')}, Genre: {book.get('genre')}\n, Year: {book.get('published_year')}")
                                        else:
                                            print(f"ID: {book.book_id}, Title: {book.title}\n, Author: {book.author}, Genre: {book.genre}\n, Year: {book.published_year}")
                                else:
                                    print("No books available.")
                            elif admin_action == '5':
                                # View borrowed books
                                users_with_borrowed = User.get_all_users_with_borrowed_books()
                                if users_with_borrowed:
                                    print("Users who have borrowed books:")
                                    for user in users_with_borrowed:
                                        username = user.get('user_name', user[0]) if isinstance(user, dict) else user[0]
                                        email = user.get('email', user[1]) if isinstance(user, dict) else user[1]
                                        borrowed = user.get('borrowed_books', user[2]) if isinstance(user, dict) else user[2]
                                        print(f"Username: {username}, Email: {email}, Borrowed Books: {borrowed}")
                                else:
                                    print("No users have borrowed books.")
                            elif admin_action == '6':
                                print("Logging out of admin menu...")
                                break
                            else:
                                print("Invalid option. Please choose 1-6.")
                    else:
                        # User menu
                        while True:
                            user_obj = User.get_user_by_id(user_id)
                            print(f"Welcome {user_obj.user_name}!")
                            print("\nUser Menu:\n 1. Search for a book\n 2. Borrow a book\n 3. Download book info\n 4.Return a book\n 5. Logout")
                            print("Please choose an option:")   
                            action = input("Choose an option: ")
                            if action == '1':
                                # Search for a book by title
                                title = input("Enter the book title: ")
                                if not title.strip():
                                    print("Book title cannot be empty.")
                                    continue
                                found_books = Book.get_book_by_title(title)
                                if not found_books:
                                    print("No books found with that title.")
                                else:
                                    print(f"Found {len(found_books)} book(s). Showing up to top 3 results:\n")
                                    for i, book in enumerate(found_books[:3], 1):
                                        print(f"{i}. Title: {book.title}")
                                        print(f"   Author: {book.author}")
                                        print(f"   Genre: {book.genre}")
                                        print(f"   Published Year: {book.published_year}")
                                    try:
                                        choice = int(input("Enter the number of the book you want to view details (1-3): "))
                                        if 1 <= choice <= min(3, len(found_books)):
                                            selected_book = found_books[choice - 1]
                                            print("Book Details:")
                                            print(selected_book.to_dict())
                                        else:
                                            print("Invalid selection.")
                                    except ValueError:
                                        print("Invalid input.")
                            elif action == '2':
                                # Borrow a book (implement as needed)
                                borrowed_book_title = input("Book title to borrow : ")
                                if not borrowed_book_title.strip():
                                    print("Book title cannot be empty.")
                                    continue
                                found_books = Book.get_book_by_title(borrowed_book_title)
                                
                                if found_books:
                                    selected_book = found_books[0]
                                    # Check if is_available method exists and call it
                                    if hasattr(selected_book, 'is_available') and callable(getattr(selected_book, 'is_available')):
                                        if selected_book.is_available():
                                            # Check if user_obj has borrow_book method
                                            if hasattr(user_obj, 'borrow_book') and callable(getattr(user_obj, 'borrow_book')):
                                                user_obj.borrow_book(selected_book)
                                                print(f"You have borrowed '{selected_book.title}'.")
                                            else:
                                                print("Error: User object cannot borrow books.")
                                        else:
                                            print(f"'{selected_book.title}' is currently not available for borrowing.")
                                    else:
                                        print("Error: Book availability cannot be determined.")
                                else:
                                    print("Book not found.")
                            elif action == '3':
                                # Download book info
                                book_title = input("Enter the title of the book to download info: ")
                                if not book_title.strip():
                                    print("Book title cannot be empty.")
                                    continue
                                found_books = Book.get_book_by_title(book_title)
                                if found_books:
                                    selected_book = found_books[0]
                                    filename = f"{selected_book.title.replace(' ', '_')}_info.txt"
                                    try:
                                        with open(filename, "w", encoding="utf-8") as f:
                                            for key, value in selected_book.to_dict().items():
                                                f.write(f"{key}: {value}\n")
                                        print(f"Book info downloaded to {filename}")
                                    except Exception as e:
                                        print(f"Failed to download book info: {e}")
                                else:
                                    print("Book not found.")
                            elif action == '4':
                                return_book_title = input("Enter the title of the book you want to return: ")
                                if not return_book_title.strip():
                                    print("Book title cannot be empty.")
                                    continue
                                found_books = Book.get_book_by_title(return_book_title)
                                if found_books:
                                    selected_book = found_books[0]
                                    # Check if user_obj has return_book method
                                    if hasattr(user_obj, 'return_book') and callable(getattr(user_obj, 'return_book')):
                                        if selected_book.title in getattr(user_obj, 'borrowed_books', []):
                                            user_obj.return_book(selected_book)
                                            print(f"You have returned '{selected_book.title}'.")
                                        else:
                                            print(f"You have not borrowed '{selected_book.title}'.")
                                    else:
                                        print("Error: User object cannot return books.")
                                else:
                                    print("Book not found.")
                            elif action == '5':
                                print("Logging out of user menu...")
                                break
                            else:
                                print("Invalid option. Please choose 1-4.")
                else:
                    print("Login failed. Invalid credentials.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif option == '3':
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

def login_user(user_id, password, role):
    if role == 'admin':
        user = Admin.get_admin_by_id(user_id)
    else:
        user = User.get_user_by_id(user_id)
    if user and user.password == password:
        borrowed_books = getattr(user, 'borrowed_books', [])
        return {
            'name': user.user_name,
            'role': user.role,
            'email': user.email,
            'user_id': user.id,
            'borrowed_books': borrowed_books
        }
    return None

if __name__ == "__main__":
    main()