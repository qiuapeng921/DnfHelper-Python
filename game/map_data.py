from game import address as addr, call
from game.structure import CoordinateType


class MapData:
    mem = None

    def __init__(self, mem):
        self.mem = mem

    def encode(self, data_ptr: int, value: int):
        """加密"""
        data_ptr += 4
        data_ptr = data_ptr ^ 0x1F2A025C
        return self.mem.write_int(data_ptr, value)

    def decode(self, data_ptr: int) -> int:
        """解密"""
        value = self.mem.read_int(data_ptr)
        value = value ^ 0x1F2A025C
        value -= 4
        return value

    def get_stat(self) -> int:
        """0选角 1城镇 2选图 3图内 5选择频道"""
        return self.mem.read_int(addr.YXZTAddr)

    def is_town(self) -> bool:
        """是否城镇"""
        person_ptr = call.get_per_ptr_call(addr.RwKbAddr)
        if self.mem.read_int(person_ptr + addr.DtPyAddr) == 0:
            return True
        return False

    def is_open_door(self) -> bool:
        """是否开门"""
        person_ptr = call.get_per_ptr_call(addr.RwKbAddr)
        encode_data = self.mem.read_int(self.mem.read_int(person_ptr + addr.DtPyAddr) + 16)
        if self.decode(encode_data + addr.SfKmAddr) == 0:
            return True
        return False

    def is_boss_room(self):
        """是否boss房"""
        cut = self.get_cut_room()
        boss = self.get_boss_room()
        if cut.x == boss.x and cut.y == boss.y:
            return True

        return False

    def is_pass(self):
        rw = self.mem
        room_data = rw.read_long(rw.read_long(rw.read_long(addr.FJBHAddr) + addr.SJAddr) + addr.MxPyAddr)
        data_val = rw.ReadInt(room_data + addr.GouHuoAddr)
        if data_val == 2 or data_val == 0:
            return True

        return False

    def get_boss_room(self) -> CoordinateType:
        """获取boss房间坐标"""
        result = CoordinateType()
        rw = self.mem
        room_data = rw.read_long(rw.read_long(rw.read_long(addr.FJBHAddr) + addr.SJAddr) + addr.MxPyAddr)
        result.x = self.decode(self.mem.read_int(room_data + addr.BOSSRoomXAddr))
        result.y = self.decode(self.mem.read_int(room_data + addr.BOSSRoomYAddr))
        return result

    def get_cut_room(self) -> CoordinateType:
        """获取当前房间坐标"""
        result = CoordinateType()
        rw = self.mem
        room_data = rw.read_long(rw.read_long(rw.read_long(addr.FJBHAddr) + addr.SJAddr) + addr.MxPyAddr)
        result.x = self.mem.read_int(room_data + addr.CutRoomXAddr)
        result.y = self.mem.read_int(room_data + addr.CutRoomYAddr)
        return result

    def get_pl(self) -> int:
        """获取当前pl值"""
        return self.decode(addr.MaxPlAddr) - self.decode(addr.CutPlAddr)

    def get_role_level(self) -> int:
        """获取角色等级"""
        return self.mem.read_int(addr.JSDjAddr)

    def get_map_name(self):
        """获取地图名称"""
        pass

    def read_coordinate(self, param: int) -> CoordinateType:
        """读取坐标"""
        coordinate = CoordinateType()
        if self.mem.ReadInt(param + addr.LxPyAddr) == 273:
            ptr = self.mem.read_long(param + addr.DqZbAddr)
            coordinate.x = self.mem.read_float(ptr + 0)
            coordinate.y = self.mem.read_float(ptr + 4)
            coordinate.z = self.mem.read_float(ptr + 8)
        else:
            ptr = self.mem.read_long(param + addr.FxPyAddr)
            coordinate.x = self.mem.read_float(ptr + 32)
            coordinate.y = self.mem.read_float(ptr + 36)
            coordinate.z = self.mem.read_float(ptr + 40)

        return coordinate

    def is_dialog_a(self):
        return self.mem.read_int(addr.DHAddr) == 1

    def is_dialog_b(self):
        return self.mem.read_int(addr.DHAddrB) == 1

    def is_dialog_esc(self):
        return self.mem.read_int(addr.EscDHAddr) == 1
