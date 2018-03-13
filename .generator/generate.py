#!python

import os
import jsonpickle
from jinja2 import Environment, FileSystemLoader, select_autoescape

import sys
reload(sys)
sys.setdefaultencoding('utf8')

target = 'public_html'

if not os.path.exists('%s/books' % target):
    os.makedirs('%s/books' % target)
if not os.path.exists('%s/authors' % target):
    os.makedirs('%s/authors' % target)

with open('library.json') as lib:
    library = jsonpickle.decode(lib.read())

all_books = library['books']
all_authors = library['authors']

env = Environment(loader=FileSystemLoader('.generator'))

main_template = env.get_template('index.html')
book_template = env.get_template('book.html')
author_template = env.get_template('author.html')

with open('%s/index.html' % (target), 'w') as out:
    out.write(main_template.render(books=all_books))

for book in all_books:
    with open('%s/books/%s.html' % (target, book['id']), 'w') as out:
        out.write(book_template.render(book=book))

for author_id, author in all_authors.iteritems():
    with open('%s/authors/%s.html' % (target, author_id), 'w') as out:
        out.write(author_template.render(author=author))
