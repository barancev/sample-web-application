#!python

import os
import re
from selenium import webdriver
from jinja2 import Environment, FileSystemLoader, select_autoescape

import sys
reload(sys)
sys.setdefaultencoding('utf8')

all_books = []
all_authors = {}

driver = webdriver.Firefox(capabilities={'marionette': True, 'pageLoadStrategy': 'eager'})
#driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get("http://www.100bestbooks.ru/")
rows = driver.find_elements_by_css_selector('tr[itemprop=itemListElement]')
for row in rows:
    book_link = row.find_element_by_css_selector('a[href^=item_info]')
    book_id = re.search('\d+$', book_link.get_attribute('href')).group(0)
    author_links = row.find_elements_by_css_selector('a[itemprop=author]')
    book_authors = []
    for author_link in author_links:
        author_id = re.search('\d+$', author_link.get_attribute('href')).group(0)
        author = all_authors.get(author_id, {'id': author_id, 'name': author_link.text, 'books': []})
        author['books'].append({'id': book_id, 'title': book_link.text})
        all_authors[author_id] = author
        book_authors.append({'id': author_id, 'name': author_link.text})
    all_books.append({'id': book_id, 'title': book_link.text, 'authors': book_authors})

for book in all_books:
    driver.get('http://www.100bestbooks.ru/item_info.php?id=%s' % book['id'])
    book['citation'] = driver.find_element_by_css_selector('span[itemprop=citation]').get_attribute('innerHTML')

for author in all_authors.values():
    driver.get('http://www.100bestbooks.ru/name_info.php?id=%s' % author['id'])
    author['bio'] = driver.find_element_by_css_selector('p[itemprop=description]').get_attribute('innerHTML')

driver.quit()

target = 'public_html'

if not os.path.exists('%s/books' % target):
    os.makedirs('%s/books' % target)
if not os.path.exists('%s/authors' % target):
    os.makedirs('%s/authors' % target)

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
