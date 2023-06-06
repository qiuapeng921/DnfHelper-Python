from common import globle
from plugins.logger.console import ConsoleLog
from plugins.logger.file import FileLog
from plugins.logger.gui import GuiLog

console_log = ConsoleLog()
gui_log = GuiLog()
file_log = FileLog()


def info(msg: str, t: int):
    """
    :param msg:
    :param t: 1 系统 2 普通
    :return:
    """
    if globle.cmd == "cmd":
        if t == 1:
            console_log.info(msg)
        else:
            console_log.debug(msg)
    if globle.cmd == "gui":
        if t == 1:
            gui_log.info(msg)
        else:
            gui_log.debug(msg)
