import requests
import logging


class LNM_hedge:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = (
            "https://api.lnmarkets.com"  # placeholder for the actual lnmakets url
        )

    def hedge_position(self, delta):
        try:
            url = f"{self.base_url}/v1/hedge"

            data = {"amount": delta, "action": "buy" if delta > 0 else "sell"}

            headers = {"Authorization": f"Bearer {self.api_key}"}

            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                result = response.json()
                logging.info(f"Hedging was successful: Result: {result}")
                return result
            else:
                logging.error(
                    f"Failed to perform Hedging. Status code: {response.status_code}"
                )
                return {"error": "Couldn't place hedge:"}

        except Exception as e:
            logging.exception("Error placing hedge")
            return {"error": "Error placing hedge"}
