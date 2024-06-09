import unittest
from unittest.mock import MagicMock

from src.converters.convert import save_to_mongodb


class TestSaveToMongodb(unittest.TestCase):

    def test_save_to_mongodb(self):
        # Mock the collection
        mock_collection = MagicMock()
        mock_insert_result = MagicMock()
        mock_insert_result.inserted_id = "12345"
        mock_collection.insert_one.return_value = mock_insert_result

        save_to_mongodb(mock_collection, "test_file.txt", "This is a test text")

        # Assert
        mock_collection.insert_one.assert_called_once_with({
            "file_name": "test_file.txt",
            "text": "This is a test text"
        })


if __name__ == '__main__':
    unittest.main()
