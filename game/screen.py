import _thread
import time

from common import config
from common import logger
from game import call, init, address


class Screen:
    def __init__(self, mem, map_data):
        self.thread = None
        self._switch = False
        self.mem = mem
        self.map_data = map_data

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

        data = self.map_data.get_map_data()
        num = 0
        # 遍历地图数据
        for data.obj_tmp in range(1, data.obj_num):
            obj_ptr = map_obj.get_traversal_ptr(data.start, data.obj_tmp, 2)
            if obj_ptr is not None and obj_ptr > 0:
                obj_type_a = mem.read_int(obj_ptr + address.LxPyAddr)
                obj_camp = mem.read_int(obj_ptr + address.ZyPyAddr)
                obj_code = mem.read_int(obj_ptr + address.DmPyAddr)
                if obj_type_a == 529 or obj_type_a == 545 or obj_type_a == 273 or obj_type_a == 61440:
                    obj_blood = mem.read_long(obj_ptr + address.GwXlAddr)
                    if obj_camp > 0 and obj_code > 0 and obj_blood > 0 and obj_ptr != data.rw_addr:
                        monster = map_obj.read_coordinate(obj_ptr)
                        code = config().getint("自动配置", "技能代码")
                        harm = config().getint("自动配置", "技能伤害")
                        size = config().getint("自动配置", "技能大小")
                        number = config().getint("自动配置", "技能个数")
                        call.skill_call(data.rw_addr, code, harm, monster.x, monster.y, 0, size)
                        num = num + 1
                        if num >= number:
                            break
