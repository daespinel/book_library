import os
from config import db
from book import Book, Author

# Data to initialize database with

# Delete database file if it exists currently
if os.path.exists('books.db'):
    os.remove('books.db')

db.create_all()
