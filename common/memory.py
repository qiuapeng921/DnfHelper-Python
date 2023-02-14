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

    def ReadInt(self, address):
        return self.pm.read_int(address)

    def ReadLong(self, address):
        return self.pm.read_long(address)

    def ReadFloat(self, address):
        return self.pm.read_float(address)

    def ReadBytes(self, address, length):
        return self.pm.read_bytes(address, length)

    def WriteInt(self, address, value):
        return self.pm.write_int(address, value)

    def WriteLong(self, address, value):
        return self.pm.write_long(address, value)

    def WriteFloat(self, address, value):
        return self.pm.write_float(address, value)

    def WriteBytes(self, address, value, length):
        return self.pm.write_bytes(address, value, length)

    def memory(self):
        return self.pm
