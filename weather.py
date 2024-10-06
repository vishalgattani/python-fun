import json
import time
from collections import defaultdict
from pathlib import Path
from typing import Optional

import requests

from logger import setup_logger


class WeatherData:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon
        self.data = defaultdict(list)
        self.file = "weather_data.json"
        self.url = "https://api.open-meteo.com/v1/forecast"

    def get_weather_data(self):
        try:
            response = requests.get(
                self.url,
                params={
                    "latitude": self.lat,
                    "longitude": self.lon,
                    "current": "temperature_2m",
                },
            )
            if not response.ok:
                raise Exception(f"{response.reason}: {response.text}")
            return response.json()
        except Exception as e:
            logger.error(e)

    def collect_data(self, time_sleep: int = 10, times: int = 10):
        for _ in range(times):
            weather_data = self.get_weather_data()
            time_collected = weather_data["current"]["time"]
            temperature = weather_data["current"]["temperature_2m"]
            self.data[time_collected].append(temperature)
            logger.debug(
                f"Collected data for {time_collected} with temperature {temperature}"
            )
            time.sleep(time_sleep)
        return self.data

    def dump_data(self, data: Optional[dict] = None):
        if data:
            with open(Path.cwd() / self.file, "w") as f:
                json.dump(data, f)
        else:
            with open(Path.cwd() / self.file, "w") as f:
                json.dump(self.data, f)


if __name__ == "__main__":
    logger = setup_logger(name="weather.log")
    logger.info("Starting Weather API")
    weather_data = WeatherData(lat=51.5, lon=-0.11)
    collected_data = weather_data.collect_data(time_sleep=1, times=1)
    logger.info(collected_data)
    weather_data.dump_data()
