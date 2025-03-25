import requests
import logging

class Eclair_API:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key =api_key

    def get_channel_info(self):

        try:
            url = f"{self.base_url}/channels" #Placeholder for the real Eclair url link

            headers = {
                'Authorization': 'Bearer {sel.api_key}'
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data =response.json()
                logging.info("Successfully fetched the channel info")
                return data

            else:
                logging.error(f"Failed to retrieve channel data. Status code: {response.status_code}")
                return None

        except Exception as e:
            logging.exception("Error fetching channel data from Eclair")
            return None