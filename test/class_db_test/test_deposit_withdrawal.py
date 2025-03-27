import unittest
from unittest.mock import patch, MagicMock
from deposit_withdrawal import LNMarkets_Deposit_Withdraw  # Assuming this is the location of the class
import logging


class TestLNMarketsDepositWithdraw(unittest.TestCase):
    
    @patch('deposit_withdrawal.requests.post')
    def test_deposit_satoshis_success(self, mock_post):

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "message": "Deposit successful"}
        mock_post.return_value = mock_response

        api_key = "mock_api_key"
        lnm = LNMarkets_Deposit_Withdraw(api_key)

        result = lnm.deposit_satoshis(1000)

        self.assertEqual(result, {"status": "success", "message": "Deposit successful"})
        mock_post.assert_called_once_with(
            "https://api.lnmarkets.com/v1/deposit", 
            json={"amount": 1000}, 
            headers={"Authorization": "Bearer mock_api_key"}
        )
        logging.info("Deposit test passed successfully.")

    @patch('deposit_withdrawal.requests.post')
    def test_deposit_satoshis_failure(self, mock_post):

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        api_key = "mock_api_key"
        lnm = LNMarkets_Deposit_Withdraw(api_key)

        result = lnm.deposit_satoshis(1000)


        self.assertEqual(result, {"error": "Failed to deposit satoshis"})
        mock_post.assert_called_once_with(
            "https://api.lnmarkets.com/v1/deposit", 
            json={"amount": 1000}, 
            headers={"Authorization": "Bearer mock_api_key"}
        )
        logging.error("Deposit failure test passed.")

    @patch('deposit_withdrawal.requests.post')
    def test_deposit_satoshis_exception(self, mock_post):

        mock_post.side_effect = Exception("Network error")


        api_key = "mock_api_key"
        lnm = LNMarkets_Deposit_Withdraw(api_key)


        result = lnm.deposit_satoshis(1000)


        self.assertEqual(result, {"error": "Error during deposit"})
        logging.exception("Deposit exception test passed.")

    @patch('deposit_withdrawal.requests.post')
    def test_withdraw_satoshis_success(self, mock_post):

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "message": "Withdrawal successful"}
        mock_post.return_value = mock_response

        api_key = "mock_api_key"
        lnm = LNMarkets_Deposit_Withdraw(api_key)


        result = lnm.withdraw_satoshis(500)

        self.assertEqual(result, {"status": "success", "message": "Withdrawal successful"})
        mock_post.assert_called_once_with(
            "https://api.lnmarkets.com/v1/withdraw", 
            json={"amount": 500}, 
            headers={"Authorization": "Bearer mock_api_key"}
        )
        logging.info("Withdrawal test passed successfully.")

    @patch('deposit_withdrawal.requests.post')
    def test_withdraw_satoshis_failure(self, mock_post):

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        api_key = "mock_api_key"
        lnm = LNMarkets_Deposit_Withdraw(api_key)


        result = lnm.withdraw_satoshis(500)


        self.assertEqual(result, {"error": "Failed to withdraw satoshis"})
        mock_post.assert_called_once_with(
            "https://api.lnmarkets.com/v1/withdraw", 
            json={"amount": 500}, 
            headers={"Authorization": "Bearer mock_api_key"}
        )
        logging.error("Withdrawal failure test passed.")

    @patch('deposit_withdrawal.requests.post')
    def test_withdraw_satoshis_exception(self, mock_post):

        mock_post.side_effect = Exception("Network error")


        api_key = "mock_api_key"
        lnm = LNMarkets_Deposit_Withdraw(api_key)

        result = lnm.withdraw_satoshis(500)

        self.assertEqual(result, {"error": "Error during withdrawal"})
        logging.exception("Withdrawal exception test passed.")


if __name__ == '__main__':
    unittest.main()
