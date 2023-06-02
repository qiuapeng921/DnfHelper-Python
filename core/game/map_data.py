import logging

from common import helper, globle, logger
from core.game import address as addr, skill, map_base
from core.game import call, address
import random


def get_cross_map_coordinate(map_id):
    """获取裂缝坐标"""
    ret = globle.CoordinateType()
    if map_id == 100002964 or map_id == 100002974:  # 判断开始 (map_id ＝ 100002964 或 map_id ＝ 100002974)  # //王之摇篮
        ret.x = 2
        ret.y = 5
        return ret

    if map_id == 100002965 or map_id == 100002969:  # 判断 (map_id ＝ 100002965 或 map_id ＝ 100002969)  # //海伯伦的预言所
        ret.x = 5
        ret.y = 2
        return ret

    if map_id == 100002950 or map_id == 100002951:  # 判断 (map_id ＝ 100002950 或 map_id ＝ 100002951)  # //白色大地
        ret.x = 7
        ret.y = 2
        return ret

    if map_id == 100002952 or map_id == 100002953:  # 判断 (map_id ＝ 100002952 或 map_id ＝ 100002953)  # //圣殿贝里科蒂斯
        ret.x = 6
        ret.y = 0
        return ret

    if map_id == 100002705 or map_id == 100002706:  # 判断 (map_id ＝ 100002705 或 map_id ＝ 100002706)  # //昆法特
        ret.x = 6
        ret.y = 0
        return ret

    if map_id == 100002962 or map_id == 100002963:  # 判断 (map_id ＝ 100002962 或 map_id ＝ 100002963)  # //柯涅恩山
        ret.x = 6
        ret.y = 2
        return ret

    if map_id == 100002676 or map_id == 400001567:  # 判断 (map_id ＝ 100002676 或 map_id ＝ 400001567)  # //纳瑟乌森林
        ret.x = 5
        ret.y = 0
        return ret

    if map_id == 400001565 or map_id == 400001566:  # 判断 (map_id ＝ 400001565 或 map_id ＝ 400001566)  # //永痕之光研究所
        ret.x = 6
        ret.y = 1
        return ret
    ret = None  # 默认情况
    return ret


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

    def is_run_person(self):
        """是否跑动中"""
        return self.mem.mem.read_int(call.person_ptr() + address.DzIDAddr) == 14

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

    def into_cross_rom(self):
        """进入裂缝房间"""
        cross_coord = self.cross_room()
        if cross_coord is None:
            return
        call.drift_call(call.person_ptr(), cross_coord.x, cross_coord.y, 0, 50)

    def cross_room(self) -> object:
        """裂缝是否出现"""
        mem = self.mem
        start, end = map_base.get_map_start_and_end()
        obj_num = int((end - start) / 24)
        for obj_tmp in range(obj_num):
            cross_addr = map_base.get_address(start, obj_tmp)
            if cross_addr <= 0:
                continue
            cross_code = mem.read_int(cross_addr + address.DmPyAddr)
            '''紧急任务裂缝'''
            if cross_code == 490019076:
                cross_coord = self.read_coordinate(cross_addr)
                return cross_coord
        return None

    def get_cut_room(self) -> globle.CoordinateType:
        """获取当前房间坐标"""
        result = globle.CoordinateType()
        rw = self.mem
        # 房间数据 ＝ 读长整数 (读长整数 (读长整数 (#房间编号) ＋ #时间基址) ＋ #门型偏移)
        room_data = rw.read_long(rw.read_long(rw.read_long(addr.FJBHAddr) + addr.SJAddr) + addr.MxPyAddr)
        # 返回数据.x ＝ 读长整数 (房间数据 ＋ #当前房间X)
        result.x = self.mem.read_int(room_data + addr.CutRoomXAddr)
        # 返回数据.y ＝ 读长整数 (房间数据 ＋ #当前房间Y)
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

    # 角色位置
    def get_role_coordinate(self) -> globle.CoordinateType:
        return self.read_coordinate(call.person_ptr())

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

    # 是否对话框A
    def is_dialog_a(self):
        return self.mem.read_int(addr.DHAddr) == 1

    # 是否聊天对话框
    def is_dialog_b(self):
        return self.mem.read_int(addr.DHAddrB) == 1

    # 是否对话确认框
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

    def map_jbl(self):
        """是否加百利商店"""
        pass_map_type = self.mem.read_int(address.JblAddr)
        if pass_map_type == 1002 or pass_map_type == 1003:
            return True
        return False
