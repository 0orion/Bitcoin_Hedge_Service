import logging



def calculate_total_capacity(channel_data):

    try:
        total_capacity = 0
        for channel in channel_data:
            total_capacity += channel.get('capacity', 0)
        logging.info(f"Calculating total capacity: {total_capacity}")
        return total_capacity
    except Exception as e:
        logging.exception("Error calculating total capacity")
        return 0
