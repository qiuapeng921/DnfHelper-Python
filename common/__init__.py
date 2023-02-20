import configparser
import logging

from common import memory

ini = configparser.ConfigParser()

mem = memory.Memory()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    pass
