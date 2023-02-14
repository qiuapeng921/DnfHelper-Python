from pymem import Pymem


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
        return self.pm.read_int(address)

    def read_long(self, address):
        return self.pm.read_long(address)

    def read_float(self, address):
        return self.pm.read_float(address)

    def read_bytes(self, address, length):
        return self.pm.read_bytes(address, length)

    def write_int(self, address, value):
        return self.pm.write_int(address, value)

    def write_long(self, address, value):
        return self.pm.write_long(address, value)

    def write_float(self, address, value):
        return self.pm.write_float(address, value)

    def write_bytes(self, address, value, length):
        return self.pm.write_bytes(address, value, length)

    def allocate(self, length):
        return self.pm.allocate(length)

    def memory(self) -> Pymem:
        """
        获取Pymem实例
        """
        return self.pm
