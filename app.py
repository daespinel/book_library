from flask import Flask
from flask import render_template
import connexion
import logging
import re

# Create the application instance
app = connexion.App(__name__, specification_dir='./config/')
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO)


def main():
    # Read the swagger.yml file to configure the endpoints
    app.add_api('swagger.yml')
    app.run(host='127.0.0.1', port=7575, debug=True)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/books")
@app.route("/books/<string:book_id>")
def books(book_id=""):
    """
    This function just responds to the browser URL
    localhost:7575/books
    :return:        the rendered template "books.html"
    """
    return render_template("books.html", book_id=book_id)


@app.route("/book/<string:book_id>")
def book(book_id):
    """
    This function responds to the browser URL
    localhost:7575/books/<book_id>

    :param book_id:   Id of the book to show
    :return:            the rendered template "book.html"
    """
    return render_template("book.html", book_id=book_id)


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    main()
