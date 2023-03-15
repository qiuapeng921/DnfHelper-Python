import sys
import time
import traceback

from common import logger, conf, thread
from game import init, call, address


class Screen:
    def __init__(self, mem):
        self.thread = None
        self._switch = False
        self.mem = mem

    def screen_switch(self):
        self._switch = not self._switch
        if self._switch:
            self.thread = thread.MyThreadFunc(self.screen_thread, ())
            self.thread.start()
            logger.info("技能全屏 [ √ ]")
        else:
            self._switch = False
            self.thread.stop()
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
            except Exception as err:
                print("-----------全屏开始-----------")
                except_type, _, except_traceback = sys.exc_info()
                print(except_type)
                print(err.args)
                print(except_traceback)
                print('-----------')
                for i in traceback.extract_tb(except_traceback):
                    print(i)
                print("-----------全屏结束-----------")

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
                        code = int(code_config[1])
                        harm = int(code_config[2])
                        size = float(code_config[3])
                        call.skill_call(rw_addr, code, harm, monster.x, monster.y, 0, size)
                        num = num + 1
                        if num >= code_config[4]:
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

    def ignore_building(self, ok: bool):
        """无视建筑"""
        rd_addr = call.person_ptr()
        if ok:
            self.mem.write_int(rd_addr + address.JzCtAddr, 0)
            self.mem.write_int(rd_addr + address.DtCtAddr, 0)
        else:
            self.mem.write_int(rd_addr + address.JzCtAddr, 40)
            self.mem.write_int(rd_addr + address.DtCtAddr, 10)
