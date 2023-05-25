import logging

from common import helper, globle

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

fileLog = logging.getLogger(__name__)
fileLog.setLevel(logging.DEBUG)
fileLog.addHandler(logging.FileHandler(filename="logs/debug.log"))


def info(msg: str, t: int):
    """
    :param msg:
    :param t: 1 系统 2 普通
    :return:
    """
    if globle.cmd == "cmd":
        log.debug("{} {}".format(helper.get_now_date(), msg))
    else:
        if t == 1:
            globle.win_app.add_func_content(msg)
        else:
            globle.win_app.add_edit_content(msg)


def file(msg: str):
    log.debug("{} {}".format(helper.get_now_date(), msg))
