from common import globle
from plugins.logger.interface import LogInterface


class GuiLog(LogInterface):
    def info(self, arg):
        globle.win_app.add_func_content(arg)

    def debug(self, arg):
        globle.win_app.add_func_content(arg)

    def warning(self, arg):
        globle.win_app.add_func_content(arg)

    def error(self, arg):
        globle.win_app.add_func_content(arg)

    def critical(self, arg):
        globle.win_app.add_edit_content(arg)
