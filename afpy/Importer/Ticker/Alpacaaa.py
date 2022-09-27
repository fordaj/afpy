import hoss_agent, requests, afpy, pandas as pd

from pathlib import Path

PY_FILE_PATH = afpy.Cli().cwd(__file__)

ENDPOINT_STR = "Live_Endpoint"
ID_STR = "Live_ID"
SECRET_STR = "Live_Secret"

# ENDPOINT_STR = "Paper_Endpoint"
# ID_STR = "Paper_ID"
# SECRET_STR = "Paper_Secret"

with open(PY_FILE_PATH/"Alpaca.key") as key_file:
    for line in key_file.readlines():
        if ENDPOINT_STR in line:
            ENDPOINT = line.split(": ")[1].replace('\n','')
        elif ID_STR in line:
            ALPACA_ID = line.split(": ")[1].replace('\n','')
        elif SECRET_STR in line:
            ALPACA_SECRET = line.split(": ")[1].replace('\n','')

with open(PY_FILE_PATH/"Hoss.key") as key_file:
    HOSS_KEY = key_file.readlines()[0]


hoss_client = hoss_agent.init(HOSS_KEY)

#declare some constants used throughout
ACCOUNT_URL = "{}/v2/account".format(ENDPOINT)
ORDERS_URL = "{}/v2/orders".format(ENDPOINT)
HEADERS = {'APCA-API-KEY-ID':ALPACA_ID,
           'APCA-API-SECRET-KEY':ALPACA_SECRET}

#access account info
def get_acct_info():
	r_account = requests.get(ACCOUNT_URL, headers = HEADERS).json()
print(get_acct_info())



# #access order info
# def create_order(symbol, qty, side, type, time_in_force):
# 	PARAMS = {
#     	"symbol":symbol,
#     	"qty": qty,
#     	"side": side,
#     	"type": type,
#     	"time_in_force": time_in_force
# 	}
# 	r_order = requests.post(ORDERS_URL, json=PARAMS, headers=HEADERS)
# 	return r_order
# #make order request
# print(create_order("FB",1,"buy","market","gtc").json())

import alpaca_trade_api as tradeapi

# authentication and connection details
api_key = ALPACA_ID
api_secret = ALPACA_SECRET
base_url = 'https://api.alpaca.markets'

# instantiate REST API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# obtain account information
account = api.get_account()
print(account)


# Get daily price data for AAPL over the last 5 trading days.
barset = api.get_barset('AAPL', 'day', limit=5)
aapl_bars = barset['AAPL']

# See how much AAPL moved in that timeframe.
week_open = aapl_bars[0].o
week_close = aapl_bars[-1].c
percent_change = (week_close - week_open) / week_open * 100
print('AAPL moved {}% over the last 5 days'.format(percent_change))