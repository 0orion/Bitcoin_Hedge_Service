# Bitcoin Hedging Service

A simple implementation of a Bitcoin hedging service using the Lightning Network and LNMarkets.

## Prerequisites

- Python 3.x
- pip (Python package installer)
- An Eclair Lightning Node
- An LNMarkets account with API access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/0orion/crude-bitcoin-hedging.git
cd crude-bitcoin-hedging
```

2. Install dependencies:
```bash
pip install -r crude_requirements.txt
```

3. Configure the service:
   - Open `hedge_service.py`
   - Replace the following variables with your credentials:
     ```python
     ECLAIR_API_URL = "your_eclair_url"
     ECLAIR_API_PASSWORD = "your_eclair_password"
     LNMARKETS_API_KEY = "your_lnmarkets_key"
     LNMARKETS_API_SECRET = "your_lnmarkets_secret"
     LNMARKETS_API_PASSPHRASE = "your_lnmarkets_passphrase"
     ```

## Usage

Run the service:
```bash
python crude_hedge_service.py
```

The service will start on port 5000 and begin monitoring your Lightning Network channels.

## API Endpoints

- POST `/hedge`: Endpoint for receiving payment notifications
  - Request body: `{"channelId": "your_channel_id", "amount": amount_in_sats}`
