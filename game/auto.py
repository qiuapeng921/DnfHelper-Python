"""
自动刷图主线程
"""
import _thread
import time

from game import global_data
from game import map_data as data


class Auto:
    # 内存
    mem = None
    # 首次进图
    firstEnterMap = bool
    # 已完成角色数量
    completedRoleNum = int
    # 已完成刷图次数
    completedNum = int

    def __init__(self, mem):
        self.mem = mem

    def switch(self):
        """自动开关"""
        global_data.auto_switch = not global_data.auto_switch
        if global_data.auto_switch:
            _thread.start_new_thread(self.auto_thread, ())
            print("自动刷图 [ √ ]")
        else:
            global_data.auto_switch = False
            print("自动刷图 [ x ]")

    def auto_thread(self):
        """自动线程"""
        while global_data.auto_switch:
            time.sleep(0.2)

            # 进入城镇
            if data.get_stat() == 0:
                time.sleep(0.2)
                self.enter_town()
                continue

            # 城镇处理
            if data.get_stat() == 1 and data.is_town() == True:
                self.town_handle()
                continue

            # 进入副本
            if data.get_stat() == 2:
                self.enter_map(global_data.map_id, global_data.map_level)
                continue

            # 在地图内
            if data.get_stat() == 3:
                if self.firstEnterMap is False and data.is_town() is False:
                    # todo 透明call
                    self.start_func()
                    pass

                # 过图
                if data.is_open_door() is True and data.is_boss_room() is False:
                    pass

                # 通关
                if data.is_boss_room() is False:
                    pass

    def start_func(self):
        pass

    def enter_town(self):
        """进入城镇"""
        pass

    def town_handle(self):
        """城镇处理"""
        pass

    def select_map(self):
        """选图"""
        pass

    def enter_map(self, map_id: int, map_level: int):
        """进图"""
        pass

    def pass_map(self):
        """过图"""

    def quit_map(self):
        """出图"""
