"""
自动刷图主线程
"""
import _thread
import time

from common import logger
from game import call
from game.init import global_data, map_data


class Auto:
    # 内存
    mem = None
    # 首次进图
    firstEnterMap = False
    # 已完成角色数量
    completedRoleNum = 0
    # 已完成刷图次数
    completedNum = 0

    def __init__(self, mem):
        self.mem = mem

    @classmethod
    def switch(cls):
        """自动开关"""
        global_data.auto_switch = not global_data.auto_switch
        if global_data.auto_switch:
            _thread.start_new_thread(cls.auto_thread, ())
            logger.info("自动刷图 [ √ ]")
        else:
            global_data.auto_switch = False
            logger.info("自动刷图 [ x ]")

    @classmethod
    def auto_thread(cls):
        """自动线程"""
        while global_data.auto_switch:
            time.sleep(0.2)

            # 进入城镇
            if map_data.get_stat() == 0:
                time.sleep(0.2)
                cls.enter_town()
                continue

            # 城镇处理
            if map_data.get_stat() == 1 and map_data.is_town() is True:
                cls.town_handle()
                continue

            # 进入副本
            if map_data.get_stat() == 2:
                cls.enter_map(global_data.map_id, global_data.map_level)
                continue

            # 在地图内
            if map_data.get_stat() == 3:
                if cls.firstEnterMap is False and map_data.is_town() is False:
                    # todo 透明call
                    cls.start_func()
                    pass

                # 过图
                if map_data.is_open_door() is True and map_data.is_boss_room() is False:
                    pass

                # 通关
                if map_data.is_boss_room() is False:
                    pass

    @classmethod
    def start_func(cls):
        pass

    @classmethod
    def enter_town(cls):
        """进入城镇"""
        pass

    @classmethod
    def town_handle(cls):
        """城镇处理"""
        pass

    @classmethod
    def select_map(cls):
        """选图"""
        while 1:
            time.sleep(0.2)
            # TODO 选图
            # 不在选图界面跳出循环
            if map_data.get_stat() == 2:
                break

    @classmethod
    def enter_map(cls, map_id: int, map_level: int):
        """进图"""
        if map_level == 5:
            if map_id < 10 or map_id == 1000:
                call.go_map_call(map_id, 0)
            else:
                for i in range(4, -1, -1):
                    call.go_map_call(map_id, i)
        else:
            call.go_map_call(map_id, map_level)

        for i in range(0, 10):
            time.sleep(0.2)
            # 进图副本跳出循环
            if map_data.get_stat() == 3:
                break

    @classmethod
    def pass_map(cls):
        """过图"""
        if map_data.is_open_door() is False or map_data.is_boss_room() is True:
            return
        # todo 寻路过图

    @classmethod
    def quit_map(cls):
        """出图"""
        cls.completedNum = cls.completedNum + 1
        logger.info("副本名称 [ {} ]".format("格蓝迪发电站"))
        logger.info("自动刷图 [ {} ] 剩余疲劳 [ {} ]".format(cls.completedNum, map_data.get_pl()))
        time.sleep(0.2)

        # 翻牌
        while 1:
            time.sleep(0.2)
            # TODO 回城
            if map_data.get_stat() == 1 or map_data.is_town() is True:
                break
