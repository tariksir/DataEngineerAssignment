from zipfile import ZipFile

import pandas as pd
import requests


def get_max_date(df: pd.DataFrame) -> str:
    return df["Date"].max().strftime('%Y-%m-%d')


class DataMiner:
    """
    The DataMiner class is responsible for getting the data from the API, using the API export endpoint
    it downloads the data and stores it in a local file. The data is then read into a pandas dataframe.
    This way the online time is reduced. The data is refreshed in case the data is older than the current date at the query.
    """
    def __init__(self, url="https://api.covid19api.com/", time_period=30):
        self.data = None
        self.url: str = url
        self.time_period: int = time_period
        self.data_file_zip = "resources/data/all.zip"
        self.data_file = "resources/data/all.json"

    def init_data_file(self):
        with requests.get(self.url + "export", stream=True) as r:
            r.raise_for_status()
            with open(self.data_file_zip, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)
        with ZipFile(self.data_file_zip, 'r') as zip_f:
            zip_f.extractall(path="resources/data")

    def init_miner(self):
        self.init_data_file()
        data = pd.read_json(self.data_file)
        self.data = data[["Date", "Country", "Province", 'Confirmed', 'Deaths', 'Recovered', 'Active']]

    def refresh_data(self):
        self.init_miner()

    def get_api_status(self) -> str:
        try:
            result = requests.get(self.url)
            if result.status_code == 200:
                return "success"
            else:
                return "failed"
        except requests.exceptions.RequestException as e:
            print(e)

    def get_country_data(self, country: str, from_date: str, to_date: str) -> pd.DataFrame:
        # if the data is older than the current date at the query, refresh the data.
        if get_max_date(self.data) < to_date:
            self.refresh_data()

        country_data = self.data[self.data["Country"] == country]
        country_data = country_data[country_data["Date"] >= from_date]
        country_data = country_data[country_data["Date"] <= to_date]
        return country_data

    def get_countries_data(self, from_date: str, to_date: str) -> pd.DataFrame:
        # if the data is older than the current date at the query, refresh the data.

        if get_max_date(self.data) < to_date:
            self.refresh_data()
        countries_data = self.data[self.data["Date"] >= from_date]
        countries_data = countries_data[countries_data["Date"] <= to_date]
        return countries_data.sort_values(by=['Country', 'Date'])
