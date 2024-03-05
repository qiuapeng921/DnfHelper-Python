"""
自动刷图主线程
"""
import _thread
import random
import time

from common import config, file
from common import helper, logger
from game import call, init, address
from game import mem
from plugins.driver.button import drive_button
from plugins.driver.keyboard import *


class Auto:
    # 首次进图
    firstEnterMap = False
    # 已完成刷图次数
    completedNum = 0
    # 线程开关
    thread_switch = False
    # 线程句柄
    threadHande = None

    task = None
    traversal = None
    map_data = None
    pack = None
    game_map = None

    @classmethod
    def __init__(cls, task, traversal, map_data, pack, game_map):
        cls.task = task
        cls.traversal = traversal
        cls.map_data = map_data
        cls.pack = pack
        cls.game_map = game_map

    @classmethod
    def switch(cls):
        """自动开关"""
        init.global_data.auto_switch = not init.global_data.auto_switch
        cls.thread_switch = init.global_data.auto_switch
        if cls.thread_switch:
            cls.threadHande = _thread.start_new_thread(cls.auto_thread, ())
            logger.info("自动刷图 [ √ ]", 1)
        else:
            init.global_data.auto_switch = False
            cls.thread_switch = False
            logger.info("自动刷图 [ x ]", 1)

    @classmethod
    def auto_thread(cls):
        """自动线程"""
        while cls.thread_switch:
            try:
                time.sleep(0.3)
                if cls.map_data.is_dialog_esc() or cls.map_data.is_dialog_a() or cls.map_data.is_dialog_b():
                    drive_button(VK_ESC, 0, False)
                    time.sleep(0.2)
                    drive_button(VK_SPACE, 0, False)
                    continue

                # 进入城镇
                if cls.map_data.get_stat() == 0:
                    time.sleep(0.2)
                    cls.enter_town()
                    continue

                # 城镇处理
                if cls.map_data.get_stat() == 1 and cls.map_data.is_town() is True:
                    cls.town_handle()
                    continue

                # 进入副本
                if cls.map_data.get_stat() == 2:
                    cls.enter_map(init.global_data.map_id, init.global_data.map_level)
                    continue

                # 在地图内
                if cls.map_data.get_stat() == 3:
                    if cls.firstEnterMap is False and cls.map_data.is_town() is False:
                        # 透明call
                        call.hide_call(call.person_ptr())
                        # sss评分
                        sss_score = random.randint(5201314, 9999999)
                        mem.write_long(mem.read_long(address.PFAddr) + address.CEPfAddr, sss_score)
                        # 无视建筑
                        cls.traversal.ignore_building(True)
                        # 进图开启功能
                        cls.start_func()
                        cls.firstEnterMap = True
                        continue

                    # 跟随怪物
                    if config().getint("自动配置", "跟随打怪") > 0:
                        cls.traversal.follow_monster()

                    # 过图
                    if cls.map_data.is_open_door() is True and cls.map_data.is_boss_room() is False:
                        if cls.traversal.is_exists_item() is True:
                            # 捡物品
                            cls.traversal.pickup()
                            continue

                        # 过图
                        cls.pass_map()
                        continue

                    # 通关
                    if cls.map_data.is_boss_room() and cls.map_data.is_pass():
                        if cls.traversal.is_exists_item() is True:
                            # 捡物品
                            cls.traversal.pickup()
                            continue
                        # 关闭功能
                        cls.start_func()
                        # 关闭穿透
                        cls.traversal.ignore_building(False)
                        # 退出副本
                        cls.quit_map()
                        cls.firstEnterMap = False
            except Exception as err:
                helper.print_trace("自动线程开始", err)

    @classmethod
    def start_func(cls):
        func_mod = config().getint("自动配置", "开启功能")
        if func_mod == 1:
            print("功能1为实现")
        if func_mod == 2:
            print("功能2为实现")
        if func_mod == 3:
            print("功能3为实现")

    @classmethod
    def enter_town(cls):
        """进入城镇"""
        role_num = config().getint("自动配置", "角色数量")
        init.global_data.completed_role = init.global_data.completed_role + 1
        if init.global_data.completed_role > role_num:
            logger.info("指定角色完成所有角色", 2)
            logger.info("自动刷图 [ x ]", 2)
            cls.thread_switch = False
            init.global_data.auto_switch = False
            return

        time.sleep(0.2)
        cls.pack.select_role(init.global_data.completed_role)
        time.sleep(0.5)
        logger.info("进入角色 {} ".format(init.global_data.completed_role), 2)
        logger.info("开始第 {} 个角色,剩余疲劳 {}".format(init.global_data.completed_role + 1, cls.map_data.get_pl()),
                    2)
        while cls.thread_switch:
            time.sleep(0.2)
            # 进入城镇跳出循环
            if cls.map_data.get_stat() == 1:
                break

    @classmethod
    def town_handle(cls):
        """城镇处理"""
        if cls.map_data.get_pl() <= 8:
            cls.return_role()
            return

        time.sleep(0.5)
        # 分解装备
        cls.traversal.handle_equip()

        # 1 剧情 2 搬砖
        auto_model = config().getint("自动配置", "自动模式")
        if auto_model == 1 and cls.map_data.get_role_level() < 110:
            init.global_data.map_id = cls.task.handle_main()
            init.global_data.map_level = 0
        if auto_model == 2 and cls.map_data.get_role_level() == 110:
            map_ids = list(map(int, config().get("自动配置", "普通地图").split(",")))
            random_number = random.randint(0, len(map_ids) - 1)
            init.global_data.map_id = map_ids[random_number]
            init.global_data.map_level = config().getint("自动配置", "地图难度")

        if init.global_data.map_id == 0:
            logger.info("地图编号为空,无法切换区域", 2)
            return

        # 区域发包
        max_region = call.area_call(init.global_data.map_id)
        time.sleep(0.5)
        if cls.map_data.get_max_region() != max_region:
            logger.info("未切换到区域,检查是否完成该地图区域任务", 2)
            return

        time.sleep(0.5)
        cls.select_map()

    @classmethod
    def select_map(cls):
        """选图"""
        while cls.thread_switch:
            time.sleep(0.2)
            # 选图
            cls.pack.select_map()
            # 不在选图界面跳出循环
            if cls.map_data.get_stat() == 2:
                break

    @classmethod
    def return_role(cls):
        """返回角色"""
        logger.info("疲劳值不足 · 即将切换角色", 2)
        time.sleep(0.2)
        cls.pack.return_role()
        while cls.thread_switch:
            time.sleep(0.2)
            if cls.map_data.get_stat() == 0:
                break

    @classmethod
    def enter_map(cls, map_id: int, map_level: int):
        """进图"""
        if map_level == 5:
            # drive_button(VK_SPACE, 0, False)
            for i in range(4, -1, -1):
                if cls.map_data.get_stat() == 3:
                    break
                if cls.map_data.get_stat() == 2:
                    cls.pack.go_map(map_id, i, 0, 0)
                    time.sleep(1)
                if cls.map_data.get_stat() == 1:
                    cls.select_map()
        else:
            # drive_button(VK_SPACE, 0, False)
            cls.pack.go_map(map_id, map_level, 0, 0)

        while cls.thread_switch:
            time.sleep(0.2)
            # 进图副本跳出循环
            if cls.map_data.get_stat() == 3:
                break

    @classmethod
    def pass_map(cls):
        """过图"""
        if cls.map_data.is_open_door() is False or cls.map_data.is_boss_room() is True:
            return

        over_map = config().getint("自动配置", "过图方式")
        if over_map > 0:
            # 寻路过图
            map_data = cls.game_map.map_data()
            if len(map_data.map_route) >= 2:
                direction = cls.game_map.get_direction(map_data.map_route[0], map_data.map_route[1])
                if over_map == 1:
                    call.over_map_call(direction)
                if over_map == 2:
                    call.drift_over_map(direction)

    @classmethod
    def pass_boss(cls):
        """ 刷图次数处理 """
        cfg_name = "C:\\config.ini"
        complete_number = file.read_ini(cfg_name, "default", "count")
        complete_number = int(complete_number) + 1
        file.write_ini(cfg_name, "default", "count", complete_number)

        map_data = cls.map_data
        logger.info("{} [ {} ] 剩余疲劳 [ {} ]".format(map_data.get_map_name(), complete_number, map_data.get_pl()), 2)

    @classmethod
    def quit_map(cls):
        """出图"""
        cls.pass_boss()

        time.sleep(0.2)
        # 翻牌
        cls.pack.get_income(0, random.randint(0, 3))

        out_type = config().getint("自动配置", "出图方式")
        if out_type == 0:
            time.sleep(5)

        while cls.thread_switch:
            time.sleep(0.2)
            # 出图
            cls.pack.leave_map()
            if cls.map_data.get_stat() == 1 or cls.map_data.is_town():
                break
