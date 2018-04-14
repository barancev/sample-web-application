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
db.generate_mapping(create_tables=False)

env = Environment(loader=FileSystemLoader('.generator'))

main_template = env.get_template('index.html')
book_template = env.get_template('book.html')
add_book_template = env.get_template('add_book.html')
edit_book_template = env.get_template('edit_book.html')
author_template = env.get_template('author.html')
add_author_template = env.get_template('add_author.html')
edit_author_template = env.get_template('edit_author.html')

urls = (
    '/add_book', 'add_book',
    '/edit_book/(.*)', 'edit_book',
    '/edit_book', 'edit_book',
    '/delete_book/(.*)', 'delete_book',
    '/book/(.*)', 'book',
    '/add_author', 'add_author',
    '/edit_author/(.*)', 'edit_author',
    '/edit_author', 'edit_author',
    '/delete_author/(.*)', 'delete_author',
    '/author/(.*)', 'author',
    '/.*', 'index'
)

app = web.application(urls, globals())

class index:
    @db_session
    def GET(self):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        return main_template.render(books=Book.select())

class add_book:
    @db_session
    def GET(self):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        return add_book_template.render()

    @db_session
    def POST(self):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        data = web.input(submit=None)
        book = Book(title=data.title, citation=data.citation)
        author = Author.get(_id=data.author)
        commit()
        raise web.seeother("book/%s" % book._id)

class edit_book:
    @db_session
    def GET(self, book_id):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        book = Book.get(_id=book_id)
        return edit_book_template.render(book=book, authors=Author.select(), book_authors=[author._id for author in book.authors])

    @db_session
    def POST(self):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        data = web.input(submit=None, authors=[])
        book = Book.get(_id=data.book_id)
        book.title = data.title
        book.citation = data.citation
        book.authors.clear()
        for author_id in data.authors:
            book.authors.add(Author.get(_id=author_id))
        commit()
        raise web.seeother("book/%s" % book._id)

class delete_book:
    @db_session
    def GET(self, book_id):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        Book.get(_id=book_id).delete()
        commit()
        raise web.seeother("/")

class book:
    @db_session
    def GET(self, book_id):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        return book_template.render(book=Book.get(_id=book_id))

class add_author:
    @db_session
    def GET(self):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        return add_author_template.render()

    @db_session
    def POST(self):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        data = web.input(submit=None)
        author = Author(name=data.name, bio=data.bio)
        commit()
        raise web.seeother("author/%s" % author._id)

class edit_author:
    @db_session
    def GET(self, author_id):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        return edit_author_template.render(author=Author.get(_id=author_id))

    @db_session
    def POST(self):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        data = web.input(submit=None)
        author = Author.get(_id=data.author_id)
        author.name = data.name
        author.bio = data.bio
        commit()
        raise web.seeother("author/%s" % author._id)

class delete_author:
    @db_session
    def GET(self, author_id):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        Author.get(_id=author_id).delete()
        commit()
        raise web.seeother("/")

class author:
    @db_session
    def GET(self, author_id):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        return author_template.render(author=Author.get(_id=author_id))

if __name__ == '__main__':
    app.run()
