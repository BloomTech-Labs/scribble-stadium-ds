import preprocess_directory
import unittest
FIXTURES_DIRECTORY_PATH = "Fixtures"

class TestGetImages(unittest.TestCase):
    """
    Class for test function below for the get_all_images function from the preprocess_directory.py file
    """
    def test_check_file(self):
        """
        Test for the get_all_images function from the preprocess_directory.py file, verifying images are in the file.
        """
        result = preprocess_directory.get_all_images(FIXTURES_DIRECTORY_PATH)
        self.assertEqual(1, len(result))
        self.assertTrue("test2.jpg" in result[0])


if __name__ == '__main__':
    unittest.main()

