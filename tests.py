import unittest
import subprocess
import os
from config import STORAGE_FILEPATH, REQUIRED_FIELDS
from ms import parse_args, get_movie_details


class MovieServiceBaseTest:

    def run_script(self, args):
        return subprocess.run(
            'python ms.py ' + ' '.join(args),
            capture_output=True
        )


class MovieServiceFunctionalTests(unittest.TestCase, MovieServiceBaseTest):

    def test_download_movie_data_and_save_to_json_file(self):
        args = ["the matrix", "lord of the rings"]
        self.assertEqual(self.run_script(args).returncode, 0)
        # self.assertTrue(os.path.isfile(STORAGE_FILEPATH))


class MovieServiceUnitTests(unittest.TestCase, MovieServiceBaseTest):

    def test_argument_parser(self):
        args = ["the matrix", "lord of the rings"]
        self.assertEqual(args, parse_args(args).list)

    def test_get_movie_details(self):
        """This test might be prone to failures due to data changes
        on the website. In case it fails make sure that the
        expected_output is up to date."""

        title = "the matrix"
        expected_output = {
            'imdbID': 'tt0133093',
            'Title': 'The Matrix',
            'imdbRating': '8.7',
            'BoxOffice': '$171,479,930'
        }
        rv = get_movie_details(title, REQUIRED_FIELDS)
        self.assertDictEqual(expected_output, rv)


if __name__ == "__main__":
    unittest.main()
