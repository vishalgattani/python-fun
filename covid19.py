import json
from collections import defaultdict
from pathlib import Path
from typing import Optional

import requests

from logger import setup_logger


class CovidData:
    def __init__(self):
        self.url = "https://disease.sh/v3/covid-19/"
        self.data = defaultdict(list)
        self.file = "covid19_data.json"

    def get_endpoints(self, url: str = "https://disease.sh/apidocs/swagger_v3.json"):
        try:
            response = requests.get(url)
            if not response.ok:
                raise Exception(f"{response.reason}: {response.text}")
            logger.debug(response.json())
            return response.json()
        except Exception as e:
            logger.error(e)
            logger.exception(e)
            return None

    def get_covid_cases(self, country: str = "usa", *args, **kwargs):
        try:
            response = requests.get(self.url + f"countries/{country}", params=kwargs)
            if not response.ok:
                raise Exception(f"{response.reason}: {response.text}")
            self.data[country] = response.json()
            return response.json()
        except Exception as e:
            logger.error(e)
            logger.exception(e)
            return None

    def get_all_covid_cases(self, country: str = "usa", *args, **kwargs):
        try:
            response = requests.get(self.url + f"historical/{country}", params=kwargs)
            if not response.ok:
                raise Exception(f"{response.reason}: {response.text}")
            self.data = response.json()
            return response.json()
        except Exception as e:
            logger.error(e)
            logger.exception(e)
            return None

    def dump_data(self, data: Optional[dict] = None):
        if data:
            with open(Path.cwd() / self.file, "w") as f:
                json.dump(data, f)
        else:
            with open(Path.cwd() / self.file, "w") as f:
                json.dump(self.data, f)


if __name__ == "__main__":
    logger = setup_logger(name="covid19.log")
    logger.info("Starting Covid API")
    covid_data = CovidData()
    covid_data.get_endpoints()
    covid_data.get_covid_cases(country="usa")
    covid_data.get_all_covid_cases(country="usa", lastdays=10)
    covid_data.dump_data()
