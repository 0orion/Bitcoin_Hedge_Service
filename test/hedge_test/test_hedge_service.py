import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
from hedge_service import app  # Import the Flask app
from class_LNM import LNMarkets_Deposit_Withdraw


class TestHedgeService(unittest.TestCase):
    @patch('hedge_service.LNMarkets_Deposit_Withdraw')
    @patch('hedge_service._deposit_satoshis')
    @patch('hedge_service._withdraw_satoshis')
    def test_deposit(self, mock_withdraw, mock_deposit, MockLNM):

        mock_deposit.return_value = {"status": "success", "message": "Deposit successful"}

        mock_lnm_instance = MockLNM.return_value
        mock_lnm_instance.deposit_satoshis.return_value = {"status": "success", "message": "Deposit successful"}

        client = app.test_client()


        response = client.post('/deposit', json={"amount": 1000})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "success", "message": "Deposit successful"})

        mock_lnm_instance.deposit_satoshis.assert_called_once_with(1000)

    @patch('hedge_service.LNMarkets_Deposit_Withdraw')  # Mock the LNMarkets_Deposit_Withdraw class
    @patch('hedge_service._deposit_satoshis')  # Mock the private method _deposit_satoshis
    @patch('hedge_service._withdraw_satoshis')  # Mock the private method _withdraw_satoshis
    def test_withdraw(self, mock_withdraw, mock_deposit, MockLNM):
        # Prepare mock response for withdraw_satoshis
        mock_withdraw.return_value = {"status": "success", "message": "Withdrawal successful"}
        
        # Mock the LNMarkets_Deposit_Withdraw object
        mock_lnm_instance = MockLNM.return_value
        mock_lnm_instance.withdraw_satoshis.return_value = {"status": "success", "message": "Withdrawal successful"}

        # Prepare Flask test client
        client = app.test_client()

        # Make a POST request to the /withdraw route
        response = client.post('/withdraw', json={"amount": 1000})
        
        # Test if the response is valid
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "success", "message": "Withdrawal successful"})

        # Verify the mock methods were called correctly
        mock_lnm_instance.withdraw_satoshis.assert_called_once_with(1000)

    # Add more tests as necessary for other parts of the app


if __name__ == '__main__':
    unittest.main()
