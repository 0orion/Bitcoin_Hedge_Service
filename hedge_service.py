import requests
import time
from flask import Flask, request, jsonify
import threading


print("Starting hedge service")


ECLAIR_API_URL = "http://localhost:8080"
ECLAIR_API_PASSWORD = "password123"
LNMARKETS_API_URL = "https://api.lnmarkets.com/v1"
LNMARKETS_API_KEY = "my_api_key"
LNMARKETS_API_SECRET = "my_secret"
LNMARKETS_API_PASSPHRASE = "my_passphrase"


fiat_channels = {}
total_capacity = 0
current_position = 0
last_sync_time = None


app = Flask(__name__)


def get_channels():
    print("Getting channels")
    response = requests.post(
        f"{ECLAIR_API_URL}/channels",
        headers={'Content-Type': 'application/json'},
        auth=('', ECLAIR_API_PASSWORD)
    )
    return response.json()


def sync_channels():
    print("Syncing channels")
    global fiat_channels, total_capacity
    

    channels = get_channels()

    fiat_channels = {}
    total_capacity = 0



    for channel in channels:
        channel_id = channel.get('channelId')
        capacity = channel.get('capacity', 0)
        fiat_channels[channel_id] = {
            'capacity': capacity,
            'details': channel
        }
        total_capacity += capacity
    
    print(f"Synced {len(fiat_channels)} channels, total capacity: {total_capacity}")
    



    response = requests.get(
        f"{LNMARKETS_API_URL}/futures/positions",
        headers={
            'Content-Type': 'application/json',
            'X-Api-Key': LNMARKETS_API_KEY,
            'X-Api-Secret': LNMARKETS_API_SECRET,
            'X-Api-Passphrase': LNMARKETS_API_PASSPHRASE
        }
    )
    positions = response.json()




    global current_position
    current_position = 0
    for position in positions:
        if position['status'] == 'open':
            current_position += position['margin']
    



    reserve_amount = total_capacity * 0.1
    required_hedge = total_capacity - reserve_amount


    delta = required_hedge - current_position
    


    if abs(delta) > (required_hedge * 0.05):
        print(f"Need to adjust hedge by {delta}")
        

        side = 'b' if delta > 0 else 's'
        abs_amount = abs(delta)
        
        data = {
            'type': 'l',
            'side': side,
            'leverage': 1,
            'quantity': abs_amount,
            'price': 0,
        }
        
        response = requests.post(
            f"{LNMARKETS_API_URL}/futures/positions",
            json=data,
            headers={
                'Content-Type': 'application/json',
                'X-Api-Key': LNMARKETS_API_KEY,
                'X-Api-Secret': LNMARKETS_API_SECRET,
                'X-Api-Passphrase': LNMARKETS_API_PASSPHRASE
            }
        )
        print("Adjusted hedge position")
    else:
        print("No need to adjust hedge")







@app.route('/hedge', methods=['POST'])
def hedge_endpoint():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data"}), 400
    
    channel_id = data.get('channel_id')
    amount_change = data.get('amount_change', 0)
    
    if not channel_id or amount_change == 0:
        return jsonify({"status": "error", "message": "Invalid data"}), 400
    

    if channel_id in fiat_channels:

        global total_capacity
        fiat_channels[channel_id]['capacity'] += amount_change
        total_capacity += amount_change
        
        print(f"Updated channel {channel_id} by {amount_change}")
        

        side = 'b' if amount_change > 0 else 's'
        abs_amount = abs(amount_change)
        
        data = {
            'type': 'l',
            'side': side,
            'leverage': 1,
            'quantity': abs_amount,
            'price': 0,
        }
        

        response = requests.post(
            f"{LNMARKETS_API_URL}/futures/positions",
            json=data,
            headers={
                'Content-Type': 'application/json',
                'X-Api-Key': LNMARKETS_API_KEY,
                'X-Api-Secret': LNMARKETS_API_SECRET,
                'X-Api-Passphrase': LNMARKETS_API_PASSPHRASE
            }
        )
        
        return jsonify({"status": "success", "message": "Updated"})
    else:
        print(f"Unknown channel: {channel_id}")
        return jsonify({"status": "error", "message": f"Unknown channel: {channel_id}"}), 400


def sync_thread_function():
    while True:
        try:
            sync_channels()
        except Exception as e:
            print(f"Error in sync: {e}")
        

        time.sleep(300)

if __name__ == "__main__":

    try:
        sync_channels()
    except Exception as e:
        print(f"Error in initial sync: {e}")

    thread = threading.Thread(target=sync_thread_function)
    thread.daemon = True
    thread.start()
    

    app.run(host='0.0.0.0', port=5000) 