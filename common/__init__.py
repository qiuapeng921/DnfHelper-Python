import logging
from configparser import ConfigParser

from common import memory

try:
    conf = ConfigParser()
    conf.read('helper.ini', encoding="utf-8-sig")
except Exception as e:
    print(e)
    exit()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
