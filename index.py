#!python

import os
from pony.orm import *
from jinja2 import Environment, FileSystemLoader, select_autoescape
import web

import sys
reload(sys)
sys.setdefaultencoding('utf8')

db = Database()

class Book(db.Entity):
    _id = PrimaryKey(int)
    title = Required(str)
    citation = Required(LongStr)
    authors = Set('Author')

class Author(db.Entity):
    _id = PrimaryKey(int)
    name = Required(str)
    bio = Required(LongStr)
    books = Set('Book')

db.bind(provider='mysql', host='localhost', user='root', password='', db='library')
db.generate_mapping(create_tables=False)

env = Environment(loader=FileSystemLoader('.generator'))

main_template = env.get_template('index.html')
book_template = env.get_template('book.html')
author_template = env.get_template('author.html')

urls = (
    '/books/(.*)\.html', 'book',
    '/authors/(.*).html', 'author',
    '/.*', 'index'
)

app = web.application(urls, globals())

class index:
    @db_session
    def GET(self):
        return main_template.render(books=Book.select())

class book:
    @db_session
    def GET(self, book_id):
        return book_template.render(book=Book.get(_id=book_id))

class author:
    @db_session
    def GET(self, author_id):
        return author_template.render(author=Author.get(_id=author_id))

if __name__ == '__main__':
    app.run()
