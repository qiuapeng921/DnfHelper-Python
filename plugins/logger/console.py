import logging

from plugins.logger.interface import LogInterface


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        # 为不同的日志级别定义一些颜色
        colors = {
            'DEBUG': '\033[94m',  # blue
            'INFO': '\033[92m',  # green
            'WARNING': '\033[93m',  # yellow
            'ERROR': '\033[91m',  # red
            'CRITICAL': '\033[95m'  # magenta
        }
        # 从记录中获取原始消息
        message = super().format(record)
        # 如果日志级别定义了颜色，则添加颜色代码
        if record.levelname in colors:
            color_code = colors[record.levelname]
            message = f"{color_code}{message}\033[0m"
        return message


class ConsoleLog(LogInterface):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # 使用彩色格式化程序创建控制台处理程序
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColoredFormatter('%(asctime)s %(message)s'))

        # 将控制台处理程序添加到记录器
        self.logger.addHandler(console_handler)

    def info(self, arg):
        self.logger.info(arg)

    def debug(self, arg):
        self.logger.debug(arg)

    def warning(self, arg):
        self.logger.warning(arg)

    def error(self, arg):
        self.logger.error(arg)

    def critical(self, arg):
        self.logger.critical(arg)
