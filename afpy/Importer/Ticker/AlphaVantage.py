from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.timeseries import TimeSeries
import pandas as pd

class AlphaVantage:
    def __init__(self):
        self.key = None
        self.get_time_series("SPY")

    def get_key(self) -> str:
        return open("source/Data/AlphaVantage.key").readlines()[0]

    def get_sector_performances(self) -> pd.DataFrame:
        data, meta_data = SectorPerformances(self.get_key(), output_format='pandas').get_sector()
        return data

    def get_time_series(self, ticker:str) -> pd.DataFrame:
        data, meta_data = TimeSeries(self.get_key(), output_format='pandas').get_daily(ticker,outputsize='full')
        return data