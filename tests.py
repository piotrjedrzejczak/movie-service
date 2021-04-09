import unittest
import subprocess
import os
from config import STORAGE_FILEPATH
from ms import parse_args


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


if __name__ == "__main__":
    unittest.main()