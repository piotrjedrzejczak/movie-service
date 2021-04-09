import unittest
import subprocess
import os
from config import STORAGE_FILEPATH


class MovieServiceTest(unittest.TestCase):
    
    def test_download_movie_data_and_save_to_json_file(self):
        rv = subprocess.run('python ms.py "the matrix" "lord of the rings"', capture_output=True)
        self.assertEqual(rv.returncode, 0)
        self.assertTrue(os.path.isfile(STORAGE_FILEPATH))

if __name__ == "__main__":
    unittest.main()