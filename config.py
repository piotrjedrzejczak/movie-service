import os

API_KEY = "f8501a2c"
STORAGE_FILENAME = "movies.json"
STORAGE_FILEPATH = os.path.join(os.getcwd(), STORAGE_FILENAME)
REQUIRED_FIELDS = ['imdbID', 'title', 'imdbRating', 'BoxOffice']