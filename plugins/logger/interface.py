from abc import ABC, abstractmethod


class LogInterface(ABC):
    """
    定义一个名为 LogInterface 日志 的接口
    """

    @abstractmethod
    def info(self, arg):
        pass

    @abstractmethod
    def debug(self, arg):
        pass

    @abstractmethod
    def warning(self, arg):
        pass

    @abstractmethod
    def error(self, arg):
        pass

    @abstractmethod
    def critical(self, arg):
        pass
