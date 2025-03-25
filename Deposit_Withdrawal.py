import requests
import logging

class LNMarkets_Deposit_Withdraw:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.lnmarkets.com"  # Placeholder for LNM actual url

    def deposit_satoshis(self, amount):


        try:
            url = f"{self.base_url}/v1/deposit"

            data = {
                "amount": amount # amount in sats
            }
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }

            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                result = response.json()
                loggin.info(f"Deposit successful: {result}")
                return result
            else:
                logging.error(f"Failed to deposit satoshis. Status code: {response.status_code}")
                return {"error": "Failed to deposit satoshis"}
        except Exception as e:
            logging.exception("Error during deposit")
            return {"error": "Error during deposit"}





    def withdraw_satoshis(self, amount):


        try:
            url = f"{self.base_url}/v1/withdraw"

            data = {
                "amount": amount  # amount in sats
            }
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }

            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                result = response.json()
                logging.info(f"Withdrawal successful: {result}")
                return result
            else:
                logging.error(f"Failed to withdraw satoshis. Status code: {response.status_code}")
                return {"error": "Failed to withdraw satoshis"}
        except Exception as e:
            logging.exception("Error during withdrawal")
            return {"error": "Error during withdrawal"}
