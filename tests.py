import os
import unittest
from sqlite3 import connect
from config import API_KEY, REQUIRED_FIELDS, TEST_DATABASE_URI
from ms import main, parse_args, format_movie_data, get_movie_details_by_title


class MovieServiceBaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_db_uri = TEST_DATABASE_URI
        self.connection = connect(self.test_db_uri)
        self.cursor = self.connection.cursor()

    def tearDown(self) -> None:
        self.connection.close()
        os.remove(TEST_DATABASE_URI)


class MovieServiceFunctionalTests(MovieServiceBaseTest):
    def test_download_movie_data_and_save_to_db(self):
        args = ["--list", "The Matrix", "The Lord of the Rings: The Fellowship of the Ring"]
        main(args, self.test_db_uri)
        self.cursor.execute("SELECT title FROM movies")
        records = self.cursor.fetchall()
        self.assertEqual([title[0] for title in records], args[1:])

    def test_adding_duplicate_movies_to_database(self):
        args = ["--list", "The Matrix"]
        main(args, self.test_db_uri)
        self.cursor.execute("SELECT title FROM movies")
        records = self.cursor.fetchall()
        self.assertEqual([title[0] for title in records], args[1:])
        main(args, self.test_db_uri)
        self.cursor.execute("SELECT title FROM movies")
        records = self.cursor.fetchall()
        self.assertEqual([title[0] for title in records], args[1:])

    def test_movie_list_display(self):
        args = ["--list", "The Matrix", "Casino", "Tenet"]
        main(args, self.test_db_uri)
        args = ["--display"]
        main(args, self.test_db_uri)
        self.assertTrue(1, 0)


class MovieServiceUnitTests(MovieServiceBaseTest):
    def test_argument_parser(self):
        args = ["--list", "the matrix", "lord of the rings"]
        self.assertEqual(args[1:], parse_args(args).list)

    def test_get_movie_details_by_title(self):
        """This test might be prone to failures due to data changes
        on the website. In case it fails make sure that the
        expected_output is up to date."""

        title = "the matrix"
        expected_output = {
            "imdbID": "tt0133093",
            "Title": "The Matrix",
            "imdbRating": "8.7",
            "BoxOffice": "$171,479,930",
        }
        rv = get_movie_details_by_title(title, REQUIRED_FIELDS, API_KEY)
        self.assertEqual(expected_output, rv)

    def test_try_to_find_non_existing_movie(self):
        title = "asdasdasdasdasd"
        self.assertRaises(
            LookupError, get_movie_details_by_title, title, REQUIRED_FIELDS, API_KEY
        )

    def test_raw_movie_data_formatting(self):
        raw_data = {
            "imdbID": "tt0133093",
            "Title": "The Matrix",
            "imdbRating": "8.7",
            "BoxOffice": "$171,479,930",
        }
        expected_format = ["tt0133093", "The Matrix", 8.7, 171479930]
        rv = format_movie_data(raw_data, REQUIRED_FIELDS)
        self.assertEqual(rv, expected_format)


if __name__ == "__main__":
    unittest.main(buffer=True)  # buffer=True suppresses stdout prints
