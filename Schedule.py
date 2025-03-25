from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from class_eclair import Eclair_API
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class Channel_Fetcher:

    def __init__(self, eclair_api: Eclair_API):
        self.eclair_api=eclair_api


    def fetch_chan_data(self):
        channel_data =self.eclair_api.get_channel_info()
        if channel_data is not None:
            logging.info(f"Fetched channel data: {channel_data}")
        else:
            logging.error("Failed to fetch channel data from Eclair")


def start_scheduler(eclair_api: Eclair_API):
    scheduler = BackgroundScheduler()
    fetcher = Channel_Fetcher(eclair_api)

    scheduler.add_job(fetcher.fetch_chan_data, 'interval', minutes=5)

    scheduler.start()

    logging.info("Scheduler has started and will fetch channel data every 5 minutes")


