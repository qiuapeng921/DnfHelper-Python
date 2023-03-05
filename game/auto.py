"""
自动刷图主线程
"""
import _thread
import random
import time

from common import logger, conf
from game import init, call, mem, address


class Auto:
    # 首次进图
    firstEnterMap = False
    # 已完成角色数量
    completedRoleNum = 0
    # 已完成刷图次数
    completedNum = 0
    # 线程开关
    thread_switch = False

    def __init__(self):
        pass

    @classmethod
    def switch(cls):
        """自动开关"""
        init.global_data.auto_switch = not init.global_data.auto_switch
        if init.global_data.auto_switch:
            _thread.start_new_thread(cls.auto_thread, ())
            logger.info("自动刷图 [ √ ]")
        else:
            init.global_data.auto_switch = False
            logger.info("自动刷图 [ x ]")

    @classmethod
    def auto_thread(cls):
        """自动线程"""
        while init.global_data.auto_switch:
            time.sleep(0.2)

            # 进入城镇
            if init.map_data.get_stat() == 0:
                time.sleep(0.2)
                cls.enter_town()
                continue

            # 城镇处理
            if init.map_data.get_stat() == 1 and init.map_data.is_town() is True:
                cls.town_handle()
                continue

            # 进入副本
            if init.map_data.get_stat() == 2:
                cls.enter_map(init.global_data.map_id, init.global_data.map_level)
                continue

            # 在地图内
            if init.map_data.get_stat() == 3:
                if cls.firstEnterMap is False and init.map_data.is_town() is False:
                    # 透明call
                    call.hide_call(call.person_ptr())
                    time.sleep(0.1)
                    # sss评分
                    mem.write_long(mem.read_long(address.PFAddr) + address.CEPfAddr, 999999)
                    cls.start_func()
                    cls.firstEnterMap = True

                # 跟随怪物
                if conf.getint("自动配置", "跟随打怪") == 1:
                    # todo FollowMonster()
                    pass

                # 过图
                if init.map_data.is_open_door() is True and init.map_data.is_boss_room() is False:
                    cls.pass_map()
                    continue

                # 通关
                if init.map_data.is_boss_room() is False:
                    if init.map_data.is_boss_room():
                        # PackPickup()
                        cls.start_func()
                        time.sleep(0.2)
                        cls.quit_map()
                        cls.firstEnterMap = False

    @classmethod
    def start_func(cls):
        pass

    @classmethod
    def enter_town(cls):
        """进入城镇"""
        role_num = conf.getint("自动配置", "角色数量")
        cls.completedRoleNum = cls.completedRoleNum + 1
        if cls.completedRoleNum > role_num:
            logger.info("指定角色完成所有角色")
            logger.info("自动刷图 [ x ]")
            cls.thread_switch = False
            init.global_data.auto_switch = False
            return

        time.sleep(0.2)
        init.pack.select_role(1)
        time.sleep(0.5)
        logger.info("进入角色 {} ".format(1))
        logger.info("开始第 {} 个角色,剩余疲劳 [ %d ]".format(1 + 1), init.map_data.get_pl())
        while cls.thread_switch:
            time.sleep(0.2)
            # 进入城镇跳出循环
            if init.map_data.get_stat() == 1:
                break

    @classmethod
    def town_handle(cls):
        """城镇处理"""
        if init.map_data.get_pl() <= 8:
            cls.return_role()
            return

        time.sleep(0.2)
        # TODO 分解装备

        # 1 剧情 2 搬砖
        auto_model = conf.getint("自动配置", "自动模式")
        if auto_model == 1 and init.map_data.get_role_level() < 110:
            init.global_data.map_id = 104
            init.global_data.map_id = 0

        if auto_model == 2 and init.map_data.get_role_level() == 110:
            map_ids = conf.get("自动配置", "地图编号").split(",")
            random_number = random.randint(0, len(map_ids) - 1)
            init.global_data.map_id = map_ids[random_number]
            init.global_data.map_id = conf.getint("自动配置", "地图难度")

        time.sleep(0.2)
        call.area_call(init.globle.GlobalData.map_id)

    @classmethod
    def select_map(cls):
        """选图"""
        while cls.thread_switch:
            time.sleep(0.2)
            # 选图
            init.pack.select_map()
            # 不在选图界面跳出循环
            if init.map_data.get_stat() == 2:
                break

    @classmethod
    def return_role(cls):
        """返回角色"""
        logger.info("疲劳值不足 · 即将切换角色")
        time.sleep(0.2)
        init.pack.return_role()
        while cls.thread_switch:
            time.sleep(0.2)
            if init.map_data.get_stat() == 0:
                break

    @classmethod
    def enter_map(cls, map_id: int, map_level: int):
        """进图"""
        if map_level == 5:
            if map_id < 10 or map_id == 1000:
                init.pack.go_map(map_id, 0, 0, 0)
            else:
                init.pack.go_map(map_id, 4, 0, 0)
                init.pack.go_map(map_id, 3, 0, 0)
                init.pack.go_map(map_id, 2, 0, 0)
                init.pack.go_map(map_id, 1, 0, 0)
                init.pack.go_map(map_id, 0, 0, 0)
        else:
            init.pack.go_map(map_id, map_level, 0, 0)

        for i in range(0, 10):
            time.sleep(0.2)
            # 进图副本跳出循环
            if init.map_data.get_stat() == 3:
                break

    @classmethod
    def pass_map(cls):
        """过图"""
        if init.map_data.is_open_door() is False or init.map_data.is_boss_room() is True:
            return
        # 寻路过图
        map_data = init.game_map.map_data()
        if len(map_data.map_route) > 2:
            direction = init.game_map.get_direction((map_data.map_route[0], map_data.map_route[1]))
            over_map = conf.getint("自动配置", "过图")
            if over_map == 1:
                call.over_map_call(direction)
            if over_map == 2:
                print("未实现")

    @classmethod
    def quit_map(cls):
        """出图"""
        cls.completedNum = cls.completedNum + 1
        logger.info("副本名称 [ {} ]".format("格蓝迪发电站"))
        logger.info("自动刷图 [ {} ] 剩余疲劳 [ {} ]".format(cls.completedNum, init.map_data.get_pl()))
        time.sleep(0.2)
        # 翻牌
        init.pack.get_income()

        while True:
            time.sleep(0.2)
            # 出图
            init.pack.leave_map()
            if init.map_data.get_stat() == 1 or init.map_data.is_town() is True:
                break
