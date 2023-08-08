import _thread
import time

from common import config, helper
from common import logger
from game import call, init, address
from game import skill


class Screen:
    def __init__(self, mem):
        self.thread = None
        self._switch = False
        self.mem = mem

    def screen_switch(self):
        self._switch = not self._switch
        if self._switch:
            self.thread = _thread.start_new_thread(self.screen_thread, ())
            logger.info("技能全屏 [ √ ]", 1)
        else:
            self._switch = False
            logger.info("技能全屏 [ x ]", 1)

    def screen_thread(self):
        while self._switch:
            self.full_screen()
            time.sleep(0.3)

    @classmethod
    def screen_kill(cls):
        """秒杀完毕"""
        call.skill_call(0, 54141, 0, 0, 0, 0, 1.0)
        logger.info("秒杀完毕 [ √ ]", 1)

    def full_screen(self):
        """全屏遍历"""
        mem = self.mem
        map_obj = init.map_data
        if map_obj.get_stat() != 3:
            return

        rw_addr = call.person_ptr()
        map_data = mem.read_long(mem.read_long(rw_addr + address.DtPyAddr) + 16)
        start = mem.read_long(map_data + address.DtKs2)
        end = mem.read_long(map_data + address.DtJs2)
        obj_num = int((end - start) / 24)
        num = 0
        for obj_tmp in range(obj_num):
            obj_ptr = mem.read_long(start + obj_tmp * 24)
            obj_ptr = mem.read_long(obj_ptr + 16) - 32
            if obj_ptr > 0:
                obj_type_a = mem.read_int(obj_ptr + address.LxPyAddr)
                obj_camp = mem.read_int(obj_ptr + address.ZyPyAddr)
                obj_code = mem.read_int(obj_ptr + address.DmPyAddr)
                if obj_type_a == 529 or obj_type_a == 545 or obj_type_a == 273 or obj_type_a == 61440:
                    obj_blood = mem.read_long(obj_ptr + address.GwXlAddr)
                    if obj_camp > 0 and obj_code > 0 and obj_blood > 0 and obj_ptr != rw_addr:
                        monster = map_obj.read_coordinate(obj_ptr)
                        code = config().getint("自动配置", "技能代码")
                        harm = config().getint("自动配置", "技能伤害")
                        size = config().getint("自动配置", "技能大小")
                        number = config().getint("自动配置", "技能个数")
                        call.skill_call(rw_addr, code, harm, monster.x, monster.y, 0, size)
                        num = num + 1
                        if num >= number:
                            break

    def follow_monster(self):
        """跟随怪物"""
        mem = self.mem
        map_obj = init.map_data
        if map_obj.get_stat() != 3:
            return

        rw_addr = call.person_ptr()
        map_data = mem.read_long(mem.read_long(rw_addr + address.DtPyAddr) + 16)
        start = mem.read_long(map_data + address.DtKs2)
        end = mem.read_long(map_data + address.DtJs2)
        obj_num = int((end - start) / 24)
        for obj_tmp in range(obj_num):
            obj_ptr = mem.read_long(start + obj_tmp * 24)
            obj_ptr = mem.read_long(obj_ptr + 16) - 32
            if obj_ptr > 0:
                obj_type_a = mem.read_int(obj_ptr + address.LxPyAddr)
                if obj_type_a == 529 or obj_type_a == 545 or obj_type_a == 273 or obj_type_a == 61440:
                    obj_camp = mem.read_int(obj_ptr + address.ZyPyAddr)
                    obj_code = mem.read_int(obj_ptr + address.DmPyAddr)
                    obj_blood = mem.read_long(obj_ptr + address.GwXlAddr)
                    if obj_camp > 0 and obj_ptr != rw_addr:
                        monster = map_obj.read_coordinate(obj_ptr)
                        if obj_blood > 0:
                            call.drift_call(rw_addr, monster.x, monster.y, 0, 2)
                            time.sleep(0.2)
                            if config().getint("自动配置", "跟随打怪") == 2:
                                title = helper.get_process_name()
                                if title == "地下城与勇士：创新世纪":
                                    keys = skill.pick_key()
                                    helper.key_press(keys, 0.3)
                            if config().getint("自动配置", "跟随打怪") == 3:
                                call.skill_call(rw_addr, 70231, 99999, monster.x, monster.y, 0, 1.0)

    def ignore_building(self, ok: bool):
        """无视建筑"""
        rd_addr = call.person_ptr()
        if ok:
            self.mem.write_int(rd_addr + address.JzCtAddr, 0)
            self.mem.write_int(rd_addr + address.DtCtAddr, 0)
        else:
            self.mem.write_int(rd_addr + address.JzCtAddr, 40)
            self.mem.write_int(rd_addr + address.DtCtAddr, 10)
