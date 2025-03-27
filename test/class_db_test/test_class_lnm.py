import unittest
from unittest.mock import patch, MagicMock
from src.class_lnm import LNM_hedge
import logging


class TestLNMHedge(unittest.TestCase):

    def setUp(self):
        self.api = LNM_hedge(api_key="test_api_key")

    @patch('requests.post')

    def test_hedge_position_success(self, mock_post):

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "Hedging successful"}
        mock_post.return_value = mock_response

        result = self.api.hedge_position(1000)

        self.assertEqual(result, {"result": "Hedging successful"})
        mock_post.assert_called_once_with(
            "https://api.lnmarkets.com/v1/hedge",
            json={"amount": 1000, "action": "buy"},
            headers={"Authorization": "Bearer test_api_key"}
        )
        logging.info("Test for successful hedge position passed.")

    @patch('requests.post')
    def test_hedge_position_failure(self, mock_post):

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        result = self.api.hedge_position(-1000)

        self.assertEqual(result, {"error": "Couldn't place hedge:"})
        mock_post.assert_called_once_with(
            "https://api.lnmarkets.com/v1/hedge",
            json={"amount": -1000, "action": "sell"},
            headers={"Authorization": "Bearer test_api_key"}
        )
        logging.error("Test for failed hedge position passed.")

    @patch('requests.post')
    def test_hedge_position_exception(self, mock_post):
        mock_post.side_effect = Exception("Connection Error")
