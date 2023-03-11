from configparser import ConfigParser

try:
    conf = ConfigParser()
    conf.read('helper.ini', encoding="utf-8-sig")
except Exception as e:
    print(e)
    exit()
