CREATE TABLE book (
  id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  citation TEXT NOT NULL,
  PRIMARY KEY (id)
) DEFAULT CHARSET=utf8;

CREATE TABLE author (
  id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  bio TEXT NOT NULL,
  PRIMARY KEY (id)
) DEFAULT CHARSET=utf8;

CREATE TABLE book_author (
  book_id INT(10) UNSIGNED NOT NULL,
  author_id INT(10) UNSIGNED NOT NULL,
  PRIMARY KEY (book_id, author_id)
) DEFAULT CHARSET=utf8;
