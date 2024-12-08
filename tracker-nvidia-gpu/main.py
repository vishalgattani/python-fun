"""Nvidia GPU tracker.

For more queries, use the following command:

nvidia-smi --help-query-gpu
"""

import logging
import subprocess
import threading 
from typing import List

# set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s - %(message)s (%(filename)s:%(lineno)d)")
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
fh = logging.FileHandler(f"{__file__}.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)

def get_gpu_info()->List:
    """Runs nvidia-smi and returns the gpu memory used.

    Returns:
        List: List of gpu memory used.
    """
    gpu_info = []
    try:
        gpu_info = [x.strip() for x in subprocess.check_output("nvidia-smi --query-gpu=memory.used --format=csv", shell=True, encoding='utf-8').split("\n") if x ]
        logger.debug(f"GPU info: {gpu_info}")
    except Exception as e:
        logger.error(f"Error while getting GPU info: {e}")
    finally:
        return gpu_info

def main(sleep_time:int=5):
    """This function calls itself every 5 secs and print the gpu_memory.

    Args:
        sleep_time (int, optional): Duratin between two calls. Defaults to 5.
    """
    logger.info("Nvidia GPU tracker initializing...")
    threading.Timer(sleep_time,main).start()
    _ = get_gpu_info()
    
if __name__ == "__main__":
    main(sleep_time=5)