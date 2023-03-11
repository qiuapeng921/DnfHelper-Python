import _thread
import time

from common import logger, conf
from game import init, call, address


class Screen:
    def __init__(self, mem):
        self._switch = False
        self.mem = mem

    def screen_switch(self):
        self._switch = not self._switch
        if self._switch:
            _thread.start_new_thread(self.screen_thread, ())
            logger.info("技能全屏 [ √ ]")
        else:
            self._switch = False
            logger.info("技能全屏 [ x ]")

    def screen_thread(self):
        while self._switch:
            code_config = list(map(int, conf.get("自动配置", "全屏配置").split(",")))
            if len(code_config) != 5:
                logger.info("全屏配置错误")
                break
            rate = code_config[0]
            time.sleep(rate / 1000)
            try:
                self.full_screen(code_config)
            except Exception as e:
                print(e.args)

    @classmethod
    def screen_kill(cls):
        """秒杀完毕"""
        call.skill_call(0, 54141, 0, 0, 0, 0, 1.0)
        logger.info("秒杀完毕 [ √ ]")

    def full_screen(self, code_config):
        """全屏遍历"""
        mem = self.mem
        map_obj = init.map_data
        if map_obj.get_stat() != 3:
            return

        data = init.globle.Traversal()
        data.rw_addr = call.person_ptr()
        data.map_data = mem.read_long(mem.read_long(data.rw_addr + address.DtPyAddr) + 16)
        data.start = mem.read_long(data.map_data + address.DtKs2)
        data.end = mem.read_long(data.map_data + address.DtJs2)
        data.obj_num = int((data.end - data.start) / 24)
        num = 0
        for data.obj_tmp in range(data.obj_num):
            data.obj_ptr = mem.read_long(data.start + data.obj_tmp * 24)
            data.obj_ptr = mem.read_long(data.obj_ptr + 16) - 32
            if data.obj_ptr > 0:
                data.obj_type_a = mem.read_int(data.obj_ptr + address.LxPyAddr)
                data.obj_camp = mem.read_int(data.obj_ptr + address.ZyPyAddr)
                data.obj_code = mem.read_int(data.obj_ptr + address.DmPyAddr)
                if data.obj_type_a == 529 or data.obj_type_a == 545 or data.obj_type_a == 273 or data.obj_type_a == 61440:
                    data.obj_blood = mem.read_long(data.obj_ptr + address.GwXlAddr)
                    if data.obj_camp > 0 and data.obj_code > 0 and data.obj_blood > 0 and data.obj_ptr != data.rw_addr:
                        monster_coordinate = map_obj.read_coordinate(data.obj_ptr)
                        code = code_config[1]
                        harm = code_config[2]
                        size = code_config[3]
                        call.skill_call(data.rw_addr, code, harm, monster_coordinate.x, monster_coordinate.y, 0,
                                        float(size))
                        num = num + 1
                        if num >= code_config[4]:
                            break

    def follow_monster(self):
        """跟随怪物"""
        mem = self.mem
        map_obj = init.map_data
        if map_obj.get_stat() != 3:
            return

        data = init.globle.Traversal()
        data.rw_addr = call.person_ptr()
        data.map_data = mem.read_long(mem.read_long(data.rw_addr + address.DtPyAddr) + 16)
        data.start = mem.read_long(data.map_data + address.DtKs2)
        data.end = mem.read_long(data.map_data + address.DtJs2)
        data.obj_num = int((data.end - data.start) / 24)
        for data.obj_tmp in range(data.obj_num):
            data.obj_ptr = mem.read_long(data.start + data.obj_tmp * 24)
            data.obj_ptr = mem.read_long(data.obj_ptr + 16) - 32
            if data.obj_ptr > 0:
                data.obj_type_a = mem.read_int(data.obj_ptr + address.LxPyAddr)
                if data.obj_type_a == 529 or data.obj_type_a == 545 or data.obj_type_a == 273 or data.obj_type_a == 61440:
                    data.obj_camp = mem.read_int(data.obj_ptr + address.ZyPyAddr)
                    data.obj_code = mem.read_int(data.obj_ptr + address.DmPyAddr)
                    data.obj_blood = mem.read_long(data.obj_ptr + address.GwXlAddr)
                    if data.obj_camp > 0 and data.obj_ptr != data.rw_addr:
                        monster = map_obj.read_coordinate(data.obj_ptr)
                        if data.obj_blood > 0:
                            call.drift_call(data.rw_addr, monster.x, monster.y, 0, 2)
                            time.sleep(0.3)
