class MapData:
    mem = None

    def __init__(self, mem):
        self.mem = mem

    def encode(self, data_ptr: int, value: int):
        """加密"""
        data_ptr += 4
        data_ptr = data_ptr ^ 0x1F2A025C
        return self.mem.WriteInt(data_ptr, value)

    def decode(self, data_ptr: int):
        """解密"""
        value = self.mem.read_int(data_ptr)
        value = value ^ 0x1F2A025C
        value -= 4
        pass

    def get_stat(self):
        pass

    def is_town(self):
        pass

    def is_open_door(self):
        pass

    def is_boss_room(self):
        pass

    def is_pass(self):
        pass

    def get_boss_room(self):
        pass

    def get_pl(self):
        pass

    def get_role_level(self):
        pass

    def get_map_name(self):
        pass

    def read_coordinate(self):
        """读取坐标"""
        pass

    def is_dialog_a(self):
        """"""
        pass

    def is_dialog_b(self):
        """"""
        pass

    def is_dialog_esc(self):
        """"""
        pass
