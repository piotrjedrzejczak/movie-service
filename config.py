import os

DATABASE_NAME = "movies.db"
DATABASE_URI = os.path.join(os.getcwd(), DATABASE_NAME)
TEST_DATABASE_URI = os.path.join(os.getcwd(), "test_db.db")

API_KEY = "f8501a2c"

# Order and amount of these fields has to match the database schema.
REQUIRED_FIELDS = ['imdbID', 'Title', 'imdbRating', 'BoxOffice']

# SQL Query Templates
SELECT_ALL_TITLES = "SELECT title FROM movies"
SELECT_AVARAGE_RATING = "SELECT AVG(rating) FROM movies"
SELECT_HIGHEST_RATED_MOVIE = "SELECT title, rating, boxoffice FROM movies WHERE rating = (SELECT MAX(rating) FROM movies)" # noqa
SELECT_HIGHEST_BOXOFFICE = "SELECT title, rating, boxoffice FROM movies WHERE rating = (SELECT MAX(boxoffice) FROM movies)" # noqa
CHECK_IF_MOVIES_TABLE_EXIST = "SELECT name FROM sqlite_master WHERE type='table' AND name='movies'"
CREATE_MOVIES_TABLE = "CREATE TABLE movies (id TEXT, title TEXT, rating TEXT, boxoffice TEXT, PRIMARY KEY (id))" # noqa
INSERT_INTO_MOVIES_TABLE = "INSERT INTO movies (id, title, rating, boxoffice) VALUES (?, ?, ?, ?)"
UPDATE_MAIN_TABLE_RECORD = "UPDATE movies SET title = ?, rating = ?, boxoffice = ? WHERE id = ?"
