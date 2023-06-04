import _thread
import datetime
import random
import time

from common import config, helper
from common import logger
from core.game import call, init, address, map_base, person_base
from core.game import call, init, address, skill


class Screen:
    person_run = False

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
            try:
                code_config = list(map(int, config().get("自动配置", "全屏配置").split(",")))
                if len(code_config) != 5:
                    logger.info("全屏配置错误", 2)
                    break
                rate = code_config[0]
                time.sleep(rate / 1000)
                self.full_screen(code_config)
            except Exception as e:
                print(e)

    @classmethod
    def screen_kill(cls):
        skill_switch = config().getint("自动配置", "全屏开关")
        if skill_switch == 0:
            return
        """秒杀完毕"""
        call.skill_call(0, 54141, 0, 0, 0, 0, 1.0)
        logger.info("秒杀完毕 [ √ ]", 1)

    def full_screen(self, code_config):
        skill_type = config().getint("自动配置", "使用技能")
        """全屏遍历"""
        mem = self.mem
        map_obj = init.map_data
        if map_obj.get_stat() != 3:
            return

        code = int(code_config[1])
        harm = int(code_config[2])
        size = float(code_config[3])
        num = int(code_config[2])

        rw_addr = call.person_ptr()
        monster_map = map_base.map_has_monster()
        for key, value in monster_map.items():
            # 地址
            target_addr = key
            # 位置
            monster = value
            if target_addr == 0 or monster is None:
                return
            obj_blood = mem.read_long(target_addr + address.GwXlAddr)
            if obj_blood > 0:
                if skill_type == 0:
                    for i in range(num):
                        call.skill_call(rw_addr, code, harm, monster.x, monster.y, 0, size)
                elif skill_type == 1:
                    call.skill_call_power([])

    def follow_monster_base(self):
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
        skill_type = config().getint("自动配置", "使用技能")
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
                            if skill_type == 1:
                                title = helper.get_process_name()
                                if title == "地下城与勇士：创新世纪":
                                    keys = skill.pick_key()
                                    helper.key_press_release_list(keys)
                            if skill_type == 0:
                                call.skill_call(rw_addr, 70231, 99999, monster.x, monster.y, 0, 1.0)

    def follow_monster(self):
        """跟随怪物"""
        mem = self.mem
        map_obj = init.map_data
        if map_obj.get_stat() != 3:
            return

        skill_type = config().getint("自动配置", "使用技能")
        supper_skill_str = config().get("自动配置", "觉醒技能")
        supper_skill_list = supper_skill_str.split(",")
        # 地图怪物信息
        monster_map = map_base.map_has_monster()
        if len(monster_map) == 0:
            return
        cross_map = map_obj.cross_room()
        if len(cross_map) > 0 >= len(monster_map):
            return
            # 地址
        obj_blood = 100000
        while obj_blood > 200 and map_obj.is_open_door() is False and len(monster_map) > 0:
            rw_addr = call.person_ptr()
            target_addr = next(iter(monster_map))
            # 位置
            monster = monster_map[target_addr]
            if target_addr == 0 or monster is None:
                return
            call.drift_call(rw_addr, monster.x, monster.y, 0, 2)
            time.sleep(0.3)
            if skill_type == 0:
                '''特效'''
                time.sleep(0.2)
                call.skill_call(rw_addr, 70231, 99999, monster.x, monster.y, 0, 1.0)
            if skill_type == 1:
                '''技能'''
                call.skill_call_power(supper_skill_list)
            obj_blood = mem.read_long(target_addr + address.GwXlAddr)
            # 重新获取怪物信息
            monster_map = map_base.map_has_monster()

    def ignore_building(self, ok: bool):
        """无视建筑"""
        rd_addr = call.person_ptr()
        if ok:
            self.mem.write_int(rd_addr + address.JzCtAddr, 0)
            self.mem.write_int(rd_addr + address.DtCtAddr, 0)
        else:
            self.mem.write_int(rd_addr + address.JzCtAddr, 40)
            self.mem.write_int(rd_addr + address.DtCtAddr, 10)

    @classmethod
    def check_break(cls, temp_time, coordinate):
        if person_base.get_action_id() == 0:
            return True
        if coordinate != map_base.get_current_room():
            return True
        if init.map_data.is_open_door() is False:
            return True
        if helper.calculate_current_time_difference(temp_time) > 10:
            return True

        return False
