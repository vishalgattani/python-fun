from typing import Optional

import requests
from logger import setup_logger

logger = setup_logger(name="sample.log")


def get_request(url: str, id: int = 1):
    try:
        url = url + str(id)
        response = requests.get(url + str(id))
        if not response.ok:
            raise Exception(f"{response.reason}: {response.text}")
        logger.debug(response.json())
        return response.json()
    except Exception as e:
        logger.error(e)
        logger.exception(e)
        return None


def post_request(url: str, id: int = 101, data: Optional[dict] = None):
    try:
        url = url + str(id)
        response = requests.post(url, data=data)
        if not response.ok:
            raise Exception(f"{response.reason}: {response.text}")
        logger.debug(response.json())
        return response.json()
    except Exception as e:
        logger.error(e)
        logger.exception(e)
        return None


def put_request(url: str, id: int = 1, data: Optional[dict] = None):
    try:
        url = url + str(id)
        response = requests.put(url, data=data)
        if not response.ok:
            raise Exception(f"{response.reason}: {response.text}")
        logger.debug(response.text)
        logger.debug(response.json())
        return response.json()
    except Exception as e:
        logger.error(e)
        logger.exception(e)
        return None


def main():
    logger.info("Starting Sample API")
    url = "https://jsonplaceholder.typicode.com/posts/"
    get_request(url, id=1)
    post_request(url, id="")
    post_request(url, id="", data={"title": "test", "body": "test"})
    get_request(url)
    put_request(url, id=1, data={"title": "test", "body": "test2"})
    get_request(url)


if __name__ == "__main__":
    main()
