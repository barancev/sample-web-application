#!python

import os
import jsonpickle
from jinja2 import Environment, FileSystemLoader, select_autoescape
import web

import sys
reload(sys)
sys.setdefaultencoding('utf8')

with open('library.json') as lib:
    library = jsonpickle.decode(lib.read())

all_books = library['books']
all_authors = library['authors']

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
    def GET(self):
        return main_template.render(books=all_books)

class book:
    def GET(self, book_id):
        return book_template.render(book=next(book for book in all_books if book['id'] == book_id))

class author:
    def GET(self, author_id):
        return author_template.render(author=all_authors[author_id])

if __name__ == '__main__':
    app.run()
