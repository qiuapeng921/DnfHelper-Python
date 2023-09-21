from configparser import ConfigParser


def config():
    conf = ConfigParser()
    conf.read('helper.ini', encoding="utf-8-sig")
    return conf
