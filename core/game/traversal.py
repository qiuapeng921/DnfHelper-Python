import _thread
import datetime
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
        monster, target_addr = map_base.map_has_monster()
        if target_addr == 0 or monster is None:
            return
        obj_blood = mem.read_long(target_addr + address.GwXlAddr)
        if obj_blood > 0:
            if skill_type == 0:
                for i in range(num):
                    call.skill_call(rw_addr, code, harm, monster.x, monster.y, 0, size)
            elif skill_type == 1:
                call.skill_call_power([])

    def follow_monster(self):
        """跟随怪物"""
        mem = self.mem
        map_obj = init.map_data
        if map_obj.get_stat() != 3:
            return

        skill_type = config().getint("自动配置", "使用技能")
        rw_addr = call.person_ptr()
        monster, target_addr = map_base.map_has_monster()
        if target_addr == 0 or monster is None:
            return
        obj_blood = mem.read_long(target_addr + address.GwXlAddr)
        if obj_blood > 0:
            call.drift_call(rw_addr, monster.x, monster.y, 0, 2)
        if skill_type == 0:
            '''特效'''
            time.sleep(0.2)
            call.skill_call(rw_addr, 70231, 99999, monster.x, monster.y, 0, 1.0)
        if skill_type == 1:
            '''技能'''
            supper_skill_str = config().get("自动配置", "觉醒技能")
            supper_skill_list = supper_skill_str.split(",")
            call.skill_call_power(supper_skill_list)
        return

    def ignore_building(self, ok: bool):
        """无视建筑"""
        rd_addr = call.person_ptr()
        if ok:
            self.mem.write_int(rd_addr + address.JzCtAddr, 0)
            self.mem.write_int(rd_addr + address.DtCtAddr, 0)
        else:
            self.mem.write_int(rd_addr + address.JzCtAddr, 40)
            self.mem.write_int(rd_addr + address.DtCtAddr, 10)

    # 寻门跑动
    @classmethod
    def find_door(cls, x, y, person_addr):
        if person_base.get_action_id() != 0:
            return
        if cls.person_run is True:
            return
        # 房间位置
        coordinate = map_base.get_current_room()

        map_obj = init.map_data
        person_location = map_obj.get_role_coordinate()
        # 横向时间 ＝ 取绝对值 (目标坐标X － 取坐标位置 (人物指针).x) ÷ 0.365
        x_time = abs(x - map_base.read_coordinate(call.person_ptr())) / 0.365
        # 纵向时间 ＝ 取绝对值 (目标坐标Y － 取坐标位置 (人物指针).y) ÷ 0.132
        y_time = abs(y - map_base.read_coordinate(call.person_ptr())) / 0.132
        # 计次x ＝ 5000
        x_count = 5000
        # 计次y ＝ 5000
        y_count = 5000
        # 两点距离 ＝ 计算距离 (取坐标位置 (人物指针).x, 取坐标位置 (人物指针).y, 目标坐标X, 目标坐标Y)
        distance = helper.distance(map_base.read_coordinate(call.person_ptr()),
                                   map_base.read_coordinate(call.person_ptr()), x, y)
        # 判断 (取坐标位置 (人物指针).x ＞ 目标坐标X 且 取绝对值 (取坐标位置 (人物指针).y － 目标坐标Y) ≤ 18 且 取绝对值 (取坐标位置 (人物指针).y － 目标坐标Y) ≥ 0)  ' 向左跑
        left = person_location.x > x and 18 >= abs(person_location.y - y) \
               and abs(person_location.y - y) >= 0
        if left:
            # 判断 (两点距离 ＞ 60)
            if distance > 60:
                # PressDown (#左光标键)
                helper.key_press_release(helper.左)
                # PressDown (#左光标键, 1)
                helper.key_press(helper.左)
                # PressDown (#左光标键, 1)
                helper.key_press(helper.左)
            # 比对时间 ＝ 取现行时间 ()
            temp_time = time.time()
            # 判断循环首 (取坐标位置 (人物指针).x － 目标坐标X ≥ 0)
            while map_obj.get_role_coordinate().x - x >= 0:
                # 判断 (取绝对值 (目标坐标X － 取坐标位置 (人物指针).x) ≤ 18
                if abs(map_obj.get_role_coordinate().y - y) <= 18:
                    break
                # 或 取游戏状态 () ≠ 3 或 取动作ID () ＝ 0
                if person_base.get_action_id() == 0:
                    break
                # 或 房间位置 ≠ 取当前房间 ()
                if coordinate != map_base.get_current_room():
                    break
                #  或 取是否开门 () ＝ 假
                if init.map_data.is_open_door() is False:
                    break
                # 或 到整数 (取时间间隔 (取现行时间 (), 比对时间, #秒)) ≥ 10)
                if helper.calculate_current_time_difference(temp_time) > 10:
                    break
                # 如果真 (两点距离 ＞ 60)
                if distance > 60:
                    # 如果真 (取动作ID () ＝ 0)
                    if person_base.get_action_id() == 0:
                        # 弹起键盘 ()
                        helper.stop_run()
                        # PressDown (#左光标键)
                        helper.key_press_release(helper.左)
                        # PressDown (#左光标键, 1)
                        helper.key_press(helper.左)
            # 判断循环尾 ()
            helper.stop_run()
        person_location = map_obj.get_role_coordinate()
        right = person_location.x < x and abs(person_location.y - y) <= 18 and abs(person_location.y - y) >= 0
        if right:
            # 左跑动
            if distance > 60:
                helper.run_right(10)
            temp_time = time.time()
            while map_obj.get_role_coordinate().x - x < 0:
                if abs(map_obj.get_role_coordinate().y - y) <= 18:
                    break
                if cls.check_break(temp_time, coordinate):
                    break
                if distance > 60:
                    if person_base.get_action_id() == 0:
                        helper.stop_run()
                        helper.run_right(10)
            helper.stop_run()
        person_location = map_obj.get_role_coordinate()
        up = abs(map_obj.get_role_coordinate().x - x) <= 18 and abs(
            person_location.x - x) >= 0 and person_location.y - y <= 18 and person_location.y - y >= 0
        if up:
            # 上跑动
            helper.run_top(10)
            temp_time = time.time()
            while map_obj.get_role_coordinate().y - y >= 0:
                if abs(map_obj.get_role_coordinate().y - y) <= 18:
                    break
                if cls.check_break(temp_time, coordinate):
                    break
                if distance > 60:
                    if person_base.get_action_id() == 0:
                        helper.stop_run()
                        helper.run_top(10)
            helper.stop_run()
        person_location = map_obj.get_role_coordinate()

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
