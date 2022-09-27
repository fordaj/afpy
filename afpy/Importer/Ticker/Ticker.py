from logging import error
import alpaca_trade_api as tradeapi
import requests
from pathlib import Path
from multipledispatch import dispatch
from typing import List

class MarketData:
    supported_apis = ["Alpaca"]
    api = {}
    def __init__(self, key_file_path:Path):
        if "Alpaca" in self.supported_apis:
            self.
        if alpaca_key_file_path != None:
            self.api["Alpaca"] = Alpaca(alpaca_key_file_path)
            self.api_status["Alpaca"] = self.api["Alpaca"].
        self.is_alpaca_api_up = self.alpaca.ping()

        pass

    @dispatch(ticker=str)
    def get_tradeability_status(self, ticker:str)->bool:
        # api = tradeapi.REST()
        # asset = api.get_asset('tickers')
        # if asset.tradable:
        #     return True
        return False
    
    @dispatch(tickers=list)
    def get_tradeability_status(self, tickers:list)->dict:
        status = {}
        for ticker in tickers:
            status[ticker] = self.get_tradeability_status(ticker)
        return status

    @dispatch(ticker=str)
    def get_current_data(self, ticker:str)->dict:
        #TODO: Get data from Alpaca
        return {}

    @dispatch(tickers=list)
    def get_current_data(self, tickers:list)->dict:
        data = {}
        for ticker in tickers:
            data[ticker] = self.get_current_data(ticker)
        return data

    @dispatch(ticker=str, timespan=list)
    def get_previous_data(self, ticker:str, timespan:list)->dict:
        import alpaca_trade_api as tradeapi

        api = tradeapi.REST()

        # Get daily price data for AAPL over the last 5 trading days.
        barset = api.get_barset('AAPL', 'day', limit=5)
        aapl_bars = barset['AAPL']

        # See how much AAPL moved in that timeframe.
        week_open = aapl_bars[0].o
        week_close = aapl_bars[-1].c
        percent_change = (week_close - week_open) / week_open * 100
        print('AAPL moved {}% over the last 5 days'.format(percent_change))
        return {}

    @dispatch(tickers=list, timespan=list)
    def get_previous_data(self, tickers:list, timespan:list)->dict:
        data = {}
        for ticker in tickers:
            data[ticker] = self.get_current_data(ticker)
        return data



a = MarketData()

print("")

class Alpaca:
    is_live = None

    def __init__(self, path_to_key_file:Path, mode="live"):
        self.path_to_key_file = path_to_key_file
        self.__parse_key_file(path_to_key_file)
        mode.lower()
        if mode == "live":
            self.is_live = True
        elif mode == "paper":
            self.is_live = False
        self.api = tradeapi.REST(
            self.alpaca_id,
            self.alpaca_secret,
            self.endpoint
        )
        self.account = self.api.get_account()
        
    def print_todays_portfolio_change(self):
        self.account = self.api.get_account()
        balance_change = float(self.account.equity) - float(self.account.last_equity)
        print(f'Today\'s portfolio balance change: ${balance_change}')
        return None

    def __parse_key_file(self, path):
        if self.is_live:
            endpoint_str = "Live_Endpoint"
            id_str = "Live_ID"
            secret_str = "Live_Secret"
        else:
            endpoint_str = "Paper_Endpoint"
            id_str = "Paper_ID"
            secret_str = "Paper_Secret"

        with open(path/"Alpaca.key") as key_file:
            for line in key_file.readlines():
                if endpoint_str in line:
                    self.endpoint = line.split(": ")[1].replace('\n','')
                elif id_str in line:
                    self.alpaca_id = line.split(": ")[1].replace('\n','')
                elif secret_str in line:
                    self.alpaca_secret = line.split(": ")[1].replace('\n','')

        # with open(path/"Hoss.key") as key_file:
        #     self.hoss_key = key_file.readlines()[0]


        #declare some constants used throughout
        # self.account_url = "{}/v2/account".format(endpoint)
        # self.orders_url = "{}/v2/orders".format(endpoint)
        self.headers = {'APCA-API-KEY-ID':self.alpaca_id,
                'APCA-API-SECRET-KEY':self.alpaca_secret}
        
    def list_nas(self):
        # Get a list of all active assets.
        active_assets = self.api.list_assets(status='active')

        # Filter the assets down to just those on NASDAQ.
        nasdaq_assets = [a for a in active_assets if a.exchange == 'NASDAQ']
        print(nasdaq_assets)

    def get_tradeability_status(self, ticker:str)->bool:
        try:
            asset = self.api.get_asset(ticker)
        except:
            raise RuntimeError("Could not get information for provided ticker string")
        if asset.tradable:
            print(f'We can trade ticker {ticker}.')
            return True
        return False


    def run(self):
        pass