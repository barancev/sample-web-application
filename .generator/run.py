#!python

import os
import re
from selenium import webdriver
import jsonpickle

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

jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False, indent=2)
with open('library.json', 'w') as out:
    out.write(jsonpickle.encode({'books': all_books, 'authors': all_authors}))
