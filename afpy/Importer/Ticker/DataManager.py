from .AlphaVantage import *
from pathlib import Path

import afpy, pandas as pd

class DataManager:
    def __init__(self):
        self.av = AlphaVantage()

    def update_ticker(self):
        ticker = input("Enter a ticker (ex. SPY): ")
        file = f"{ticker}.xlsx"
        full_path = afpy.Cli().cwd(__file__)/file
        latest_data = self.av.get_time_series(ticker)
        try:
            data = pd.read_excel(full_path)
        except:
            data = pd.DataFrame()

        print("")
        

    def date_to_datetime(self, date):
        print("")