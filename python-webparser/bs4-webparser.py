from collections import defaultdict

import requests
from bs4 import BeautifulSoup
from logger import setup_logger

logger = setup_logger(name="bs4-webparser.log")


class BS4Webparser:
    def __init__(self, url: str):
        self.url = url
        self.url_text = self.get_url_text()
        self.soup = BeautifulSoup(self.url_text, "html.parser")
        self.data = defaultdict(list)

    def get_url_text(self):
        try:
            response = requests.get(self.url)
            if not response.ok:
                raise Exception(f"{response.reason}: {response.text}")
            return response.text
        except Exception as e:
            logger.error(e)
            logger.exception(e)
            return None

    def get_p(self):
        return self.soup.find_all("p")

    def get_div(self):
        return self.soup.find_all("div")


def main():
    try:
        bs4parser = BS4Webparser(url="https://realpython.github.io/fake-jobs/")
        bs4parser.get_url_text()

        job_info = defaultdict(list)
        url = "https://realpython.github.io/fake-jobs/"
        response = requests.get(url)
        if not response.ok:
            raise Exception(f"{response.reason}: {response.text}")
        soup = BeautifulSoup(response.text, "html.parser")
        # logger.debug(soup.prettify())
        ids = soup.find(id="ResultsContainer")
        jobs = ids.find_all("div", class_="card-content")
        for job in jobs:
            title_element = job.find("h2", class_="title").text.strip()
            company_element = job.find("h3", class_="company").text.strip()
            location_element = job.find("p", class_="location").text.strip()
            job_info[company_element].append({title_element: location_element})
        logger.debug(job_info)
    except Exception as e:
        logger.error(e)
        logger.exception(e)


if __name__ == "__main__":
    main()
