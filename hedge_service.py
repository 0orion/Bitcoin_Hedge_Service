from flask import Flask, request, jsonify
import logging


from class_eclair import Eclair_API
from class_LNM import LNM_hedge
from Total_cap import calculate_total_capacity
from Schedule import start_scheduler
from Deposit_Withdrawal import LNMarkets_Deposit_Withdraw



app = Flask (__name__)

reserve_percent = 0.10
reserve = calculate_total_capacity() * reserve_percent


@app.route('/hedge', methods=['POST'])
def hedge():


    try:
        data = request.json
        logging.info(f"Receieved data: {data}")

        eclair_api = Eclair_API(base_url="http://localhost:8080", api_key="Your_Eclair_API_key")
        channel_data = eclair_api.get_channel_info()


        if channel_data is None:
            loggin.erro("Failed to fetch channel data from Eclair API")
            return jsonify({"error: Failed to retrieve channel data"}), 500

        total_capacity = calculate_total_capacity(channel_data)
        delta = total_capacity - reserve

        logging.debug(f"Total capacity: {total_capacity}, Delta: {delta}")

        lnmarket_hedge = LNM_hedge(api_key="Your_LNM_API_key")
        result = lnmarket_hedge.hedge_position(delta)

        if resut.get("error"):
            logging.error(f"Hedging failed: {result['error']})
            return jsonify({"error": "Hedging failed"}), 500

        logging.info(f"Hedge successfully placed. Delta: {delta}")
        return jsonify(result), 200

    except Exception as e:
        logging.exception("An unexpected error occured while processing request")
        return jsonify({"error": "Internal Server error"}), 500

eclair_api =Eclair_API(base_url="http://localhost:8080", api_key="Your_eclair_api_key")

start_scheduler(eclair_api)


lnmarkets_api_key = 'your_lnmarkets_api_key'
lnmarkets = LNMarkets_Deposit_Withdraw(api_key=lnmarkets_api_key)


@app.route('/deposit', methods=['POST'])
def deposit():


    try:

        data = request.json
        amount = data.get('amount')
        if amount is None or amount <= 0:
            return jsonify({"error": "Invalid amount"}), 400


        result = lnmarkets.deposit_satoshis(amount)


        if result.get("error"):
            return jsonify(result), 500


        return jsonify(result), 200
    except Exception as e:
        logging.exception("Erro occurred while procesing deposit")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/withdraw', methods=['POST'])
def withdraw():


    try:
        data = request.json
        amount = data.get('amount')
        if amount is None or amount <= 0:
            return jsonify({"error": "Invalid amount"}), 400

        result = lnmarkets.withdraw_satoshis(amount)

        if result.get("error"):
            return jsonify(result), 500

        return jsonify(result), 200
    except Exception as e:
        logging.exception("Error occurred while processing withdrawal")
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)