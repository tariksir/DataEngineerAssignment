from datetime import datetime, timedelta

from resources.data import DataMiner


class Covid19Stats:
    """
    This class is responsible for the data analysis. It uses the DataMiner class to get the data from the API.

    """
    def __init__(self, url, time_period):
        self.data_miner = DataMiner(url, time_period)

    def init_data_miner(self):
        self.data_miner.init_miner()

    def get_api_status(self) -> dict[str, str]:
        try:
            return {"status": self.data_miner.get_api_status()}
        except Exception as e:
            print(e)

    def generate_dates(self):
        to_date = datetime.date(datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ")
        from_date = (datetime.now() - timedelta(days=self.data_miner.time_period)).strftime("%Y-%m-%dT%H:%M:%SZ")
        return from_date, to_date

    def get_deaths_peak(self, country: str) -> dict:

        from_date, to_date = self.generate_dates()
        pd_data = self.data_miner.get_country_data(country=country, from_date=from_date,
                                                   to_date=to_date)
        date = pd_data[["Date", "Deaths"]].set_index("Date").diff().idxmax()[0].strftime('%Y-%m-%d')
        result = {"country": country,
                  "method": "newCasesPeak",
                  "date": date,
                  "value": int(pd_data[["Date", "Deaths"]].set_index("Date").diff().max()[0])}
        return result

    def get_country_confirmed_max(self) -> dict:

        from_date, to_date = self.generate_dates()
        time_series_data = self.data_miner.get_countries_data(from_date=from_date, to_date=to_date)
        time_series_data = time_series_data[["Country", "Date", "Confirmed"]].set_index("Date")
        time_series_data = time_series_data.groupby(['Country']).agg({'Confirmed': ['max', 'min']})
        time_series_data['diff'] = time_series_data['Confirmed']['max'] - time_series_data['Confirmed']['min']
        result = {"country": time_series_data['diff'].idxmax(),
                  "method": "ConfirmedMax",
                  "value": int(time_series_data['diff'].max())}
        return result
