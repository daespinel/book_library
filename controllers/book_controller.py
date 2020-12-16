from flask import make_response, abort
from keystoneauth1.adapter import Adapter
from keystoneauth1.exceptions import ClientException
from random import seed
from random import randint
from book import Book, Author, BookSchema, AuthorSchema
from config import db
from sqlalchemy import exc
from flask.logging import default_handler
from threading import Lock
from operator import itemgetter
import copy
import math
import json
import itertools
import string
import random
import time
import requests
import logging
import ast
import threading
import concurrent.futures
import sys

app_log = logging.getLogger()

# Handler to get the list of books

def readAllBook():
    """
    This function responds to a GET request for /api/books
    with the complete lists of  books

    :return:        sorted list of books
    """
    # Create the list of books from our data
    books = Book.query.order_by(Book.book_id).all()

    # Serialize the data for the response
    book_schema = BookSchema(many=True)
    data = book_schema.dump(books).data
    
    return data

# Create a handler for our read (GET) one book by ID


def readOneBook(book_id):
    """
    This function responds to a GET request for /api/books/{book_id}
    with a single book

    :return:        book with book_id
    """
    book = Book.query.filter(Book.book_id== book_id).one_or_none()
    if book is not None:
        book_schema = BookSchema()
        data = book_schema.dump(book).data
        return data

    else:
        abort(404, "Book with ID {id} not found".format(id=id))

def createBook(book):
    """
    This function responds to a POST request for /api/books/
    with a single book creation

    :return:        freshly created book
    """
    # Taking information from the API http POST request
    start_time = time.time()
    app_log.info('Starting time: %s', start_time)
    app_log.info('Starting a new book creation request')

    book_title = book.get("title", None)
    book_author = book.get("author", None)

    author = Author.query.filter(Author.author_name== book_author).one_or_none()
    if author is None:
        author_schema = AuthorSchema()
        pre_new_author = {
            'author_name' : book_author
        }
        author = author_schema.load(pre_new_author, session=db.session).data
        db.session.add(author)

    book_schema = BookSchema()
    pre_new_book = {
        'book_title' : book_title,
    }
    new_book = book_schema.load(pre_new_book, session=db.session).data
    new_book.book_author = author
    db.session.add(new_book)
    db.session.commit()

    end_time = time.time()
    app_log.info('Creation finishing time: %s', end_time)

    return book_schema.dump(new_book).data, 201



# Handler to update an existing book

def updateBook(book_id, book):
    pass
# Handler to delete a book


def deleteBook(book_id):
    app_log.info('Starting: Deleting a book.')
    start_time = time.time()
    book = Book.query.filter(
        Book.book_id == book_id).one_or_none()
    if book is not None:
        db.session.delete(book)
        db.session.commit()

        return make_response("{id} successfully deleted".format(id=book_id), 200)

    abort(404, "Book with ID {id} not found".format(id=book_id))