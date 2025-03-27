import unittest
from unittest.mock import patch, MagicMock
from schedule import start_scheduler, Channel_Fetcher  # Assuming schedule.py is located in the same directory
from class_eclair import Eclair_API
import logging


class TestScheduler(unittest.TestCase):

    @patch('schedule.BackgroundScheduler')
    @patch.object(Channel_Fetcher, 'fetch_chan_data')
    def test_start_scheduler(self, mock_fetch_chan_data, mock_background_scheduler):

        mock_scheduler_instance = MagicMock()
        mock_background_scheduler.return_value = mock_scheduler_instance

        mock_eclair_api = MagicMock(spec=Eclair_API)

        start_scheduler(mock_eclair_api)

        mock_background_scheduler.assert_called_once()
        mock_scheduler_instance.start.assert_called_once()

        mock_scheduler_instance.add_job.assert_called_once_with(
            mock_fetch_chan_data, 'interval', minutes=5
        )

        mock_fetch_chan_data.assert_called_once()

        logging.info("Scheduler start test passed successfully.")

    @patch('schedule.BackgroundScheduler')
    @patch.object(Channel_Fetcher, 'fetch_chan_data')
    def test_scheduler_with_failed_job(self, mock_fetch_chan_data, mock_background_scheduler):

        mock_fetch_chan_data.side_effect = Exception("Failed to fetch channel data")

        mock_scheduler_instance = MagicMock()
        mock_background_scheduler.return_value = mock_scheduler_instance

        mock_eclair_api = MagicMock(spec=Eclair_API)

        start_scheduler(mock_eclair_api)

        mock_background_scheduler.assert_called_once()
        mock_scheduler_instance.start.assert_called_once()

        mock_scheduler_instance.add_job.assert_called_once_with(
            mock_fetch_chan_data, 'interval', minutes=5
        )

        mock_fetch_chan_data.assert_called_once()

        logging.exception("Scheduler job failure test passed.")

if __name__ == '__main__':
    unittest.main()
