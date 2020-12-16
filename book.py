from config import db, ma
import json
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import fields


class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.Integer,
                           primary_key=True)
    book_title = db.Column(db.String(64))
    book_author = db.relationship(
        'Author',
        backref='book',
        uselist=False 
    )


class Author(db.Model):
    __tablename__ = "author"
    author_id = db.Column(db.Integer,
                             primary_key=True)
    author_name = db.Column(db.String(64))
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))


# Book schemas for model read and write
# Book associated schema
class BookSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Book
        sqla_session = db.session
    book_author = fields.Nested(
        'BAuthorSchema', default=[], many=False)

# Parameter associated schemas
class BAuthorSchema(ma.ModelSchema):
    """
    This class exists to get around a recursion issue
    """
    author_id = fields.Int()
    book_id = fields.Int()
    author_name = fields.Str()
    
class AuthorSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Author
        sqla_session = db.session
    book = fields.Nested('AuthorBookSchema', default=None)

class AuthorBookSchema(ma.ModelSchema):
    """
    This class exists to get around a recursion issue
    """
    book_id = fields.Int()