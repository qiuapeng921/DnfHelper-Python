from configparser import ConfigParser


def config():
    conf = ConfigParser()
    return conf.read('helper.ini', encoding="utf-8-sig")
