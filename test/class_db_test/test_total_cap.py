import unittest
from unittest.mock import patch
import logging
from total_cap import calculate_total_capacity


class TestCalculateTotalCapacity(unittest.TestCase):

    @patch('logging.info')
    @patch('logging.exception')
    def test_calculate_total_capacity_success(self, mock_exception, mock_info):

        channel_data = [
            {"capacity": 1000},
            {"capacity": 2000},
            {"capacity": 1500},
        ]

        result = calculate_total_capacity(channel_data)

        self.assertEqual(result, 5500)

        mock_info.assert_called_with("Calculating total capacity: 5500")

    @patch('logging.info')
    @patch('logging.exception')
    def test_calculate_total_capacity_empty(self, mock_exception, mock_info):
        channel_data = []

        result = calculate_total_capacity(channel_data)

        self.assertEqual(result, 0)

