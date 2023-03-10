import time

from common import conf
from game import address, init, call


class Pickup:
    def __init__(self, mem, pack, map_data):
        self.mem = mem
        self.pack = pack
        self.map_data = map_data

    def pack(self):
        """
        组包捡物
        :return:
        """
        item_config = conf.getint("自动配置", "过滤物品").split(",")
        goods = list()
        mem = self.mem
        data = init.globle.Traversal()
        data.rw_addr = call.person_ptr()
        data.map_data = mem.read_long(mem.read_long(data.rw_addr + address.DtPyAddr) + 16)
        data.start = mem.read_long(data.map_data + address.DtKs2)
        data.end = mem.read_long(data.map_data + address.DtJs2)
        data.obj_num = (data.end - data.start) / 24
        for data.obj_tmp in range(data.obj_num):
            data.obj_ptr = mem.read_long(data.start + data.obj_tmp * 24)
            data.obj_ptr = mem.read_long(data.obj_ptr + 16) - 32
            data.obj_type_a = mem.read_int(data.obj_ptr + address.LxPyAddr)
            data.obj_type_b = mem.read_int(data.obj_ptr + address.LxPyAddr + 4)
            data.obj_camp = mem.read_int(data.obj_ptr + address.ZyPyAddr)
            if (data.obj_type_a == 289 or data.obj_type_b == 289) and data.obj_camp == 200:
                goods_name = mem.read_bytes(
                    mem.read_long(mem.read_long(data.obj_ptr + address.DmWpAddr) + address.WpMcAddr), 100)
                print(goods_name)
                data.ObjNameB = ""  # common.UnicodeToString(goodsNameByte)
            if data.obj_type_b in item_config:
                continue

            if data.obj_ptr != data.rw_addr:
                res_addr = self.map_data.decode(data.obj_ptr + address.FbSqAddr)
                goods.append(res_addr)

        if len(goods) > 0:
            for i in range(len(goods)):
                self.pack.ZbSq(goods[i])
                time.sleep(0.1)


class Equip:
    """
    装备
    """

    def __init__(self):
        pass

    def handle(self):
        pass
