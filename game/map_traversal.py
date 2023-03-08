import _thread
import time

from common import logger, conf
from game import init, call, mem, address


class Screen:
    def __init__(self):
        self._switch = False

    def screen_switch(self):
        self._switch = not self._switch
        if self._switch:
            _thread.start_new_thread(self.screen_thread, ())
            logger.info("技能全屏开启")
        else:
            self._switch = False
            logger.info("技能全屏关闭")

    def screen_thread(self):
        while self._switch:
            code_config = conf.getint("自动配置", "全屏配置").split(",")
            if len(code_config) != 5:
                logger.info("全屏配置错误")
                break
            rate = code_config[0]
            time.sleep(rate / 100)
            full_screen(code_config)


def screen_kill():
    """秒杀完毕"""
    call.skill_call(0, 54141, 0, 0, 0, 0, 1.0)
    logger.info("秒杀完毕 [ √ ]")


def full_screen(code_config: list):
    """全屏遍历"""
    map_obj = init.map_data.MapData(mem)
    if map_obj.get_stat() != 3:
        return

    data = init.globle.Traversal()
    data.rw_addr = call.person_ptr()
    data.MapData = mem.read_long(mem.read_long(data.rw_addr + address.DtPyAddr) + 16)
    data.Start = mem.read_long(data.MapData + address.DtKs2)
    data.End = mem.read_long(data.MapData + address.DtJs2)
    data.ObjNum = (data.End - data.Start) / 24
    num = 0
    for data.obj_tmp in range(data.ObjNum):
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
                    call.skill_call(data.rw_addr, code, harm, monster_coordinate.x, monster_coordinate.y, 0, size)
                    num = num + 1
                    if num >= code_config[4]:
                        break
