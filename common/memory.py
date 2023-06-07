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

    def read_int(self, address: int) -> int:
        try:
            return self.pm.read_int(address)
        except Exception as e:
            logger.file_log.error("read_int 地址:{},错误:{}".format(address, e.args))

    def read_long(self, address: int) -> int:
        try:
            return self.pm.read_longlong(address)
        except Exception as e:
            logger.file_log.error("read_longlong 地址:{},错误:{}".format(address, e.args))

    def read_float(self, address: int) -> float:
        try:
            return self.pm.read_float(address)
        except Exception as e:
            logger.file_log.error("read_float 地址:{},错误:{}".format(address, e.args))

    def read_bytes(self, address: int, length: int) -> bytes:
        try:
            return self.pm.read_bytes(address, length)
        except Exception as e:
            logger.file_log.error("read_bytes 地址:{},错误:{}".format(address, e.args))

    def write_int(self, address: int, value: int):
        try:
            return self.pm.write_int(address, value)
        except Exception as e:
            logger.file_log.error("write_int 地址:{} 值:{},错误:{}".format(address, value, e.args))

    def write_long(self, address: int, value: int):
        try:
            return self.pm.write_longlong(address, value)
        except Exception as e:
            logger.file_log.error("write_longlong 地址:{} 值:{},错误:{}".format(address, value, e.args))

    def write_float(self, address: int, value: float):
        try:
            return self.pm.write_float(address, value)
        except Exception as e:
            logger.file_log.error("write_float 地址:{} 值:{},错误:{}".format(address, value, e.args))

    def write_bytes(self, address: int, value: bytes):
        try:
            return self.pm.write_bytes(address, value, len(value))
        except Exception as e:
            logger.file_log.error("write_bytes 地址:{} 值:{},错误:{}".format(address, value, e.args))

    def allocate(self, length) -> int:
        return self.pm.allocate(length)
