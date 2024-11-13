import requests
from logger import setup_logger

logger = setup_logger(name="webparser.log")


def main():
    try:
        url = "https://realpython.github.io/fake-jobs/"
        response = requests.get(url)
        if not response.ok:
            raise Exception(f"{response.reason}: {response.text}")
        text = response.text
        logger.debug(f"Response text: {text}")
        content = response.content.decode("utf-8")
        logger.debug(f"Response content: {content}")
        assert text == content
    except Exception as e:
        logger.error(e)
        logger.exception(e)


if __name__ == "__main__":
    main()
