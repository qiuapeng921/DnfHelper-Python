from common import config, helper
from common import logger
from game import call, address, rand_skill
from plugins.driver.button import drive_button
from plugins.driver.keyboard import VK_X


class Traversal:
    def __init__(self, mem, pack, map_data):
        self.mem = mem
        self.pack = pack
        self.map_data = map_data

    def is_exists_item(self) -> bool:
        """
        是否存在物品
        :return: bool
        """
        if self.map_data.get_stat() != 3:
            return False

        mem = self.mem
        item_config = config().get("自动配置", "过滤物品").split(",")
        data = self.map_data.get_map_data()

        for data.obj_tmp in range(1, data.obj_num):
            obj_ptr = self.map_data.get_traversal_ptr(data.start, data.obj_tmp, 2)
            obj_type_a = mem.read_int(obj_ptr + address.LxPyAddr)
            obj_type_b = mem.read_int(obj_ptr + address.LxPyAddr + 4)
            obj_camp = mem.read_int(obj_ptr + address.ZyPyAddr)

            if (obj_type_a == 289 or obj_type_b == 289) and obj_camp == 200:
                goods_name_ptr = mem.read_long(mem.read_long(obj_ptr + address.DmWpAddr) + address.WpMcAddr)
                goods_name_byte = mem.read_bytes(goods_name_ptr, 100)
                obj_type_b_name = helper.unicode_to_ascii(list(goods_name_byte))
                if obj_type_b_name in item_config:
                    continue

                if obj_ptr != data.rw_addr:
                    return True

        return False

    def pickup(self):
        """
        组包捡物
        :return:
        """
        mem = self.mem
        item_config = config().get("自动配置", "过滤物品").split(",")
        data = self.map_data.get_map_data()
        # 遍历地图数据
        for data.obj_tmp in range(1, data.obj_num):
            obj_ptr = self.map_data.get_traversal_ptr(data.start, data.obj_tmp, 2)
            obj_type_a = mem.read_int(obj_ptr + address.LxPyAddr)
            obj_type_b = mem.read_int(obj_ptr + address.LxPyAddr + 4)
            obj_camp = mem.read_int(obj_ptr + address.ZyPyAddr)
            if (obj_type_a == 289 or obj_type_b == 289) and obj_camp == 200:
                goods_name_ptr = mem.read_long(mem.read_long(obj_ptr + address.DmWpAddr) + address.WpMcAddr)
                goods_name_byte = mem.read_bytes(goods_name_ptr, 100)
                obj_type_b_name = helper.unicode_to_ascii(list(goods_name_byte))
                if obj_type_b_name in item_config:
                    continue

                if obj_ptr != data.rw_addr:
                    res_addr = self.map_data.decode(obj_ptr + address.FbSqAddr)
                    self.pack.pick_up(res_addr)

    def follow_monster(self):
        """跟随怪物"""
        if self.map_data.get_stat() != 3:
            return

        mem = self.mem
        data = self.map_data.get_map_data()
        map_obj = self.map_data
        # 遍历地图数据
        for data.obj_tmp in range(1, data.obj_num):
            obj_ptr = map_obj.get_traversal_ptr(data.start, data.obj_tmp, 2)
            if obj_ptr is None or obj_ptr <= 0:
                continue

            obj_type_a = mem.read_int(obj_ptr + address.LxPyAddr)
            if obj_type_a == 529 or obj_type_a == 545 or obj_type_a == 273 or obj_type_a == 61440:
                obj_camp = mem.read_int(obj_ptr + address.ZyPyAddr)
                obj_code = mem.read_int(obj_ptr + address.DmPyAddr)
                obj_blood = mem.read_long(obj_ptr + address.GwXlAddr)
                if obj_camp > 0 and obj_ptr != data.rw_addr:
                    monster = map_obj.read_coordinate(obj_ptr)
                    if obj_blood > 0:
                        call.drift_call(data.rw_addr, monster.x, monster.y, 0, 2)
                        helper.sleep(200)
                        if config().getint("自动配置", "跟随打怪") == 2:
                            title = helper.get_process_name()
                            if title == "地下城与勇士：创新世纪":
                                drive_button(VK_X, 1, False)
                                helper.sleep(800)
                                drive_button(VK_X, 2, False)
                                helper.sleep(100)
                                drive_button(rand_skill(), 0, False)
                        if config().getint("自动配置", "跟随打怪") == 3:
                            call.skill_call(data.rw_addr, 70231, 99999, monster.x, monster.y, 0, 1.0)

    def ignore_building(self, ok: bool):
        """无视建筑"""
        rd_addr = call.person_ptr()
        if ok:
            self.mem.write_int(rd_addr + address.JzCtAddr, 0)
            self.mem.write_int(rd_addr + address.DtCtAddr, 0)
        else:
            self.mem.write_int(rd_addr + address.JzCtAddr, 40)
            self.mem.write_int(rd_addr + address.DtCtAddr, 10)

    def handle_equip(self):
        """处理装备"""
        handle_type = config().getint("自动配置", "处理装备")
        if handle_type == 0:
            return

        back_pack_weight = self.map_data.back_pack_weight()
        if back_pack_weight < 60:
            return

        self.pack.tidy_backpack(1, 0)
        num = 0
        mem = self.mem
        addr = mem.read_long(mem.read_long(address.BbJzAddr) + address.WplPyAddr) + 0x48  # 装备栏偏移
        for i in range(1, 56):
            equip = self.map_data.get_traversal_ptr(addr, i, 1)
            if equip is not None and equip > 0:
                equip_level = mem.read_int(equip + address.ZbPjAddr)
                name_addr = mem.read_long(equip + address.WpMcAddr)  # 装备名称
                name_bytes = list(mem.read_bytes(name_addr, 100))
                equip_name = helper.unicode_to_ascii(name_bytes)
                if equip_level in [0, 1, 2]:
                    logger.info("处理装备 {}".format(equip_name), 1)
                    self.pack.decomposition(i + 9)
                    helper.sleep(200)
                    num += 1

        self.pack.tidy_backpack(1, 0)
        logger.info("处理装备 {} 件".format(num), 1)
