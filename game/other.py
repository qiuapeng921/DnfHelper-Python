import time

from common import config, logger, helper
from game import address, call


class Pickup:
    def __init__(self, mem, pack, map_data):
        self.mem = mem
        self.pack = pack
        self.map_data = map_data

    def pickup(self):
        """
        组包捡物
        :return:
        """
        item_config = config().get("自动配置", "过滤物品").split(",")
        goods = list()
        mem = self.mem
        rw_addr = call.person_ptr()
        map_data = mem.read_long(mem.read_long(rw_addr + address.DtPyAddr) + 16)
        start = mem.read_long(map_data + address.DtKs2)
        end = mem.read_long(map_data + address.DtJs2)
        obj_num = int((end - start) / 24)
        for obj_tmp in range(obj_num):
            obj_ptr = mem.read_long(start + obj_tmp * 24)
            obj_ptr = mem.read_long(obj_ptr + 16) - 32
            obj_type_a = mem.read_int(obj_ptr + address.LxPyAddr)
            obj_type_b = mem.read_int(obj_ptr + address.LxPyAddr + 4)
            obj_camp = mem.read_int(obj_ptr + address.ZyPyAddr)
            if (obj_type_a == 289 or obj_type_b == 289) and obj_camp == 200:
                goods_name_byte = mem.read_bytes(mem.read_long(mem.read_long(obj_ptr + address.DmWpAddr) + address.WpMcAddr), 100)
                obj_type_b_name = helper.unicode_to_ascii(list(goods_name_byte))

                if obj_type_b_name in item_config:
                    continue
                if obj_ptr != rw_addr:
                    res_addr = self.map_data.decode(obj_ptr + address.FbSqAddr)
                    goods.append(res_addr)

        if len(goods) > 0:
            for i in range(len(goods)):
                self.pack.pick_up(goods[i])
                time.sleep(0.01)


class Equip:
    def __init__(self, mem, pack, map_data):
        self.mem = mem
        self.pack = pack
        self.map_data = map_data

    def handle_equip(self):
        """处理装备"""
        # if self.map_data.back_pack_weight() < 50:
        #     return

        handle_type = config().getint("自动配置", "处理装备")
        if handle_type == 0:
            return

        num = 0
        mem = self.mem
        addr = mem.read_long(mem.read_long(address.BbJzAddr) + address.WplPyAddr) + 0x48  # 装备栏偏移
        for i in range(56):
            equip = mem.read_long(mem.read_long(addr + i * 8) - 72 + 16)
            if equip > 0:
                equip_level = mem.read_int(equip + address.ZbPjAddr)
                name_addr = mem.read_long(equip + address.WpMcAddr)  # 装备名称
                equip_name = helper.unicode_to_ascii(list(mem.read_bytes(name_addr, 100)))
                if equip_level in [0, 1, 2]:
                    logger.info("处理装备 {}".format(equip_name), 1)
                    self.pack.decomposition(i + 9)
                    time.sleep(0.2)
                    num += 1
                    continue
        self.pack.tidy_backpack(1, 0)
        logger.info("处理装备 {} 件".format(num), 1)
