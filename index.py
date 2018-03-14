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
    '/book', 'book',
    '/book/(.*)', 'book_implicit',
    '/author', 'author',
    '/author/(.*)', 'author_implicit',
    '/.*', 'index'
)

app = web.application(urls, globals())

class index:
    @db_session
    def GET(self):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        return main_template.render(books=Book.select())

class book:
    @db_session
    def GET(self):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        book_id = web.input().id
        return book_template.render(book=Book.get(_id=book_id))

class book_implicit:
    @db_session
    def GET(self, book_id):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        return book_template.render(book=Book.get(_id=book_id))

class author:
    @db_session
    def GET(self):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        author_id = web.input().id
        return author_template.render(author=Author.get(_id=author_id))

class author_implicit:
    @db_session
    def GET(self, author_id):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        return author_template.render(author=Author.get(_id=author_id))

if __name__ == '__main__':
    app.run()
