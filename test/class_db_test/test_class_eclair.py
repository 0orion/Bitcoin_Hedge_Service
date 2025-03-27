import unittest
from unittest.mock import patch, MagicMock
from src.class_eclair import Eclair_API
import logging


class TestEclairAPI(unittest.TestCase):

    def setUp(self):
        self.api = Eclair_API(base_url="https://mockurl.com", api_key="test_api_key")

    @patch('requests.get')

    def test_get_channel_info_success(self, mock_get):

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"channel_info": "some_data"}
        mock_get.return_value = mock_response


        result = self.api.get_channel_info()

        self.assertEqual(result, {"channel_info": "some_data"})
        mock_get.assert_called_once_with(
            "https://mockurl.com/channels", headers={"Authorization": "Bearer test_api_key"}
        )
        logging.info("Test for successful API call passed.")

    @patch('requests.get')
    def test_get_channel_info_failure(self, mock_get):

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = self.api.get_channel_info()

        self.assertIsNone(result)
        mock_get.assert_called_once_with(
            "https://mockurl.com/channels", headers={"Authorization": "Bearer test_api_key"}
        )
        logging.error("Test for failed API call passed.")

    @patch('requests.get')
    def test_get_channel_info_exception(self, mock_get):

        mock_get.side_effect = Exception("Connection Error")

        result = self.api.get_channel_info()

        self.assertIsNone(result)
        logging.exception("Test for exception during API call passed.")


if __name__ == '__main__':
    unittest.main()
