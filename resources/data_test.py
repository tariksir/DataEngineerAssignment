import unittest

import pandas as pd

from data import DataMiner


class DataMinerTest(unittest.TestCase):
    def test_setUp(self):
        data_miner = DataMiner()
        self.assertEqual(isinstance(data_miner, DataMiner), True)
        self.assertEqual(data_miner.url, "https://api.covid19api.com/")
        self.assertEqual(data_miner.time_period, 30)


    def test_api_status(self):
        data_miner = DataMiner()
        status = data_miner.get_api_status()
        self.assertEqual(status, 200)

    def test_get_country_data(self):
        data_miner = DataMiner()
        country_data = data_miner.get_country_data(country="Israel", from_date="2022-01-01", to_date="2022-01-31")
        self.assertEqual(isinstance(country_data, pd.DataFrame))
        self.assertNotEqual(len(country_data), 0)





if __name__ == '__main__':
    unittest.main()
