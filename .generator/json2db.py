#!python

import os
import jsonpickle
from pony.orm import *

import sys
reload(sys)
sys.setdefaultencoding('utf8')

with open('library.json') as lib:
    library = jsonpickle.decode(lib.read())

all_books = library['books']
all_authors = library['authors']

db = Database()

class Book(db.Entity):
    _id = PrimaryKey(int, auto=True)
    title = Required(str)
    citation = Required(LongStr)
    authors = Set('Author')

class Author(db.Entity):
    _id = PrimaryKey(int, auto=True)
    name = Required(str)
    bio = Required(LongStr)
    books = Set('Book')

db.bind(provider='mysql', host='localhost', user='root', password='', db='library')
db.generate_mapping(create_tables=True)
#set_sql_debug(True)

with db_session:
    db_books = {}
    db_authors = {}
    for book in all_books:
        db_book = Book(_id=book['id'], title=book['title'], citation=book['citation'])
        db_books[book['id']] = db_book
    for author in all_authors.values():
        db_author = Author(_id=author['id'], name=author['name'], bio=author['bio'])
        db_authors[author['id']] = db_author
    for book in all_books:
        db_book = db_books[book['id']]
        db_book.authors = [db_authors[author_id] for author_id in [author['id'] for author in book['authors']]]
        print(db_book.authors)
    commit()
