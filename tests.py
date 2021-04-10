import os
import unittest
from sqlite3 import connect
from ms import parse_args, get_movie_details_by_title, main
from config import REQUIRED_FIELDS, TEST_DATABASE_URI


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
        args = ["The Matrix", "The Lord of the Rings: The Fellowship of the Ring"]
        main(args, self.test_db_uri)
        self.cursor.execute("SELECT title FROM movies")
        records = self.cursor.fetchall()
        self.assertEqual([title[0] for title in records], args)

    def test_adding_duplicate_movies_to_database(self):
        args = ["The Matrix"]
        main(args, self.test_db_uri)
        self.cursor.execute("SELECT title FROM movies")
        records = self.cursor.fetchall()
        self.assertEqual([title[0] for title in records], args)
        main(args, self.test_db_uri)
        self.cursor.execute("SELECT title FROM movies")
        records = self.cursor.fetchall()
        self.assertEqual([title[0] for title in records], args)


class MovieServiceUnitTests(MovieServiceBaseTest):

    def test_argument_parser(self):
        args = ["the matrix", "lord of the rings"]
        self.assertEqual(args, parse_args(args).list)

    def test_get_movie_details_by_title(self):
        """This test might be prone to failures due to data changes
        on the website. In case it fails make sure that the
        expected_output is up to date."""

        title = "the matrix"
        expected_output = ['tt0133093', 'The Matrix', '8.7', '$171,479,930']
        rv = get_movie_details_by_title(title, REQUIRED_FIELDS)
        self.assertEqual(expected_output, rv)

    def test_try_to_find_non_existing_movie(self):
        title = "asdasdasdasdasd"
        self.assertRaises(
            LookupError,
            get_movie_details_by_title,
            title,
            REQUIRED_FIELDS
        )


if __name__ == "__main__":
    unittest.main()
