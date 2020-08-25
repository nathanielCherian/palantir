# add any callbacks for palantirs prediction here

import requests
import dateutil.parser as dp
import time

def security_api() -> dict:

    r = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json") 
    data = r.json()

    api_time = dp.parse(data['time']['updatedISO'])
    unix_time = time.mktime(api_time.timetuple())

    price = data['bpi']['USD']['rate_float']

    return {"time":unix_time, "price":price}



def callback(prediction: tuple):

    """
    :param prediction: tuple (buy/sell/hold, amount_traded)

    """

    return

