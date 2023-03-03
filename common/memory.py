import pymem
from pymem import Pymem

from common import logger


class Memory:
    # 全局进程id
    processId = int
    # 读写对象
    pm = Pymem

    def __int__(self):
        pass

    def set_process_id(self, process_id):
        self.pm = Pymem(process_id)
        self.processId = process_id

    def read_int(self, address):
        try:
            return self.pm.read_int(address)
        except pymem.exception.WinAPIError as e:
            logger.error("read_int", e)

    def read_long(self, address):
        try:
            return self.pm.read_longlong(address)
        except pymem.exception.WinAPIError as e:
            logger.error("read_long", e)

    def read_float(self, address):
        try:
            return self.pm.read_float(address)
        except pymem.exception.WinAPIError as e:
            logger.error("read_float", e)

    def read_bytes(self, address, length):
        try:
            return self.pm.read_bytes(address, length)
        except pymem.exception.WinAPIError as e:
            logger.error("read_float", e)

    def write_int(self, address, value):
        return self.pm.write_int(address, value)

    def write_long(self, address, value):
        return self.pm.write_longlong(address, value)

    def write_float(self, address, value):
        return self.pm.write_float(address, value)

    def write_bytes(self, address, value):
        return self.pm.write_bytes(address, value, len(value))

    def allocate(self, length):
        return self.pm.allocate(length)
