import logging
from common import globle, helper


def info(msg):
    if globle.cmd == "cmd":
        log = logging.getLogger(__name__)
        log.setLevel(logging.DEBUG)
        log.addHandler(logging.StreamHandler())
        log.debug("{} {}\n".format(helper.get_now_date(), msg))
    else:
        globle.win_app.add_content(msg)
