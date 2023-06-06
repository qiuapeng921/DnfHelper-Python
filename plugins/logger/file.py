import logging

from plugins.logger.interface import LogInterface


class FileLog(LogInterface):
    def __init__(self):
        # 创建 logger 对象
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # 创建 FileHandler 对象
        file_handler = logging.FileHandler('debug.log')
        file_handler.setLevel(logging.DEBUG)

        # 创建 Formatter 对象
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # 添加 Formatter 对象到 FileHandler 对象中
        file_handler.setFormatter(formatter)

        # 添加 FileHandler 对象到 logger 对象中
        self.logger.addHandler(file_handler)

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
