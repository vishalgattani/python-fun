import logging


def setup_logger(name, level=logging.DEBUG):
    """Set up a logger that writes to both a log file and the console."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        file_handler = logging.FileHandler(name, mode="w")
        file_handler.setLevel(level)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger


# logger = setup_logger()

# Example usage
# logger.info("This is an info message from the weather API")
# logger.error("This is an error message from the weather API")
