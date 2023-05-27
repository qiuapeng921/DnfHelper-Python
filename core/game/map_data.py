import logging

from common import helper, globle, logger
from core.game import address as addr, skill
from core.game import call, address
import random


class MapData:
    mem = None

    def __init__(self, mem):
        self.mem = mem

    def encode(self, data_ptr: int, value: int):
        """加密"""
        # data_ptr += 4
        # data_ptr = data_ptr ^ 0x1F2A025C
        return self.mem.write_int(data_ptr, value)

    def decode(self, data_ptr: int) -> int:
        """解密"""
        value = self.mem.read_int(data_ptr)
        # value = value ^ 0x1F2A025C
        # value -= 4
        return value

    def get_stat(self) -> int:
        """0选角 1城镇 2选图 3图内 5选择频道"""
        return self.mem.read_int(addr.YXZTAddr)

    def is_town(self) -> bool:
        """是否城镇"""
        person_ptr = call.person_ptr()
        if self.mem.read_int(person_ptr + addr.DtPyAddr) == 0:
            return True
        return False

    def is_open_door(self) -> bool:
        """是否开门"""
        person_ptr = call.person_ptr()
        encode_data = self.mem.read_long(self.mem.read_long(person_ptr + addr.DtPyAddr) + 16)
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
        """是否通关"""
        rw = self.mem
        room_data = rw.read_long(rw.read_long(rw.read_long(addr.FJBHAddr) + addr.SJAddr) + addr.MxPyAddr)
        data_val = rw.read_int(room_data + addr.GouHuoAddr)
        if data_val == 2 or data_val == 0:
            return True

        return False

    def get_boss_room(self) -> globle.CoordinateType:
        """获取boss房间坐标"""
        result = globle.CoordinateType()
        rw = self.mem
        room_data = rw.read_long(rw.read_long(rw.read_long(addr.FJBHAddr) + addr.SJAddr) + addr.MxPyAddr)
        result.x = self.decode(room_data + addr.BOSSRoomXAddr)
        result.y = self.decode(room_data + addr.BOSSRoomYAddr)
        return result

    def get_cut_room(self) -> globle.CoordinateType:
        """获取当前房间坐标"""
        result = globle.CoordinateType()
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

    def get_map_name(self) -> str:
        """获取地图名称"""
        room_data = self.mem.read_long(self.mem.read_long(self.mem.read_long(
            address.FJBHAddr) + address.SJAddr) + address.MxPyAddr)
        map_byte = self.mem.read_bytes(self.mem.read_long(room_data + address.DtMcAddr), 52)
        return helper.unicode_to_ascii(map_byte)

    def read_coordinate(self, param: int) -> globle.CoordinateType:
        """读取坐标"""
        coordinate = globle.CoordinateType()
        if self.mem.read_int(param + addr.LxPyAddr) == 273:
            ptr = self.mem.read_long(param + addr.DqZbAddr)
            coordinate.x = int(self.mem.read_float(ptr + 0))
            coordinate.y = int(self.mem.read_float(ptr + 4))
            coordinate.z = int(self.mem.read_float(ptr + 8))
        else:
            ptr = self.mem.read_long(param + addr.FxPyAddr)
            coordinate.x = int(self.mem.read_float(ptr + 32))
            coordinate.y = int(self.mem.read_float(ptr + 36))
            coordinate.z = int(self.mem.read_float(ptr + 40))

        return coordinate

    def is_dialog_a(self):
        return self.mem.read_int(addr.DHAddr) == 1

    def is_dialog_b(self):
        return self.mem.read_int(addr.DHAddrB) == 1

    def is_dialog_esc(self):
        return self.mem.read_int(addr.EscDHAddr) == 1

    def back_pack_weight(self) -> int:
        """取背包负重"""
        rw_addr = call.person_ptr()
        back_pack_ptr = self.mem.read_long(rw_addr + address.WplAddr)  # 物品栏
        cut_weigh = self.decode(back_pack_ptr + address.DqFzAddr)  # 当前负重
        max_weigh = self.decode(rw_addr + address.ZdFzAddr)  # 最大负重
        result = float(cut_weigh) / float(max_weigh) * 100
        return int(result)

    def get_fame(self) -> int:
        """获取名望"""
        rw_addr = call.person_ptr()
        return self.mem.read_long(rw_addr + address.RwMwAddr)

    def get_role_name(self) -> int:
        """获取角色名字"""
        name = self.mem.read_long(address.RwName)
        name_bytes = self.mem.read_bytes(name, 100)
        str_name = helper.bytes_to_str(name_bytes, self.mem)
        return str_name

    def get_jn_name(self) -> str:
        """获取技能名字"""
        rw_addr = call.person_ptr()
        # self.mem.read_bytes(self.mem.read_long(skill_addr), 100)
        #   helper.unicode_to_ascii(self.mem.read_bytes(self.mem.read_long(rw_addr + address.JnlAddr), 100))
        try:
            return skill.skill_cool_down(self.mem)
        except Exception as e:
            print(e)
        return


