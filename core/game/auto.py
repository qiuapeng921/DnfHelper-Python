"""
自动刷图主线程
"""
import _thread
import random
import sys
import time
import traceback

from common import config
from common import helper, logger
from core.game import mem, skill, run_time
from core.game import call, init, address


class Auto:
    # 首次进图
    firstEnterMap = False
    addBuff = False
    # 已完成刷图次数
    completedNum = 0
    # 线程开关
    thread_switch = False
    # 线程句柄
    threadHande = None
    # 任务对象
    task = None

    traversal = None

    map_data = None

    pack = None

    pick = None

    equip = None

    game_map = None

    skill = None

    @classmethod
    def __init__(cls, task, traversal, map_data, pack, pick, equip, game_map, skill):
        cls.task = task
        cls.traversal = traversal
        cls.map_data = map_data
        cls.pack = pack
        cls.pick = pick
        cls.equip = equip
        cls.game_map = game_map
        cls.skill = skill

    @classmethod
    def test_func(cls):
        role_name = skill.skill_cool_down()
        logger.info("技能名称 {}".format(role_name), 1)

    @classmethod
    def hide_body(cls):
        if cls.map_data.get_stat() == 3:
            # 透明call
            logger.info("开启透明 {}", 2)
            call.hide_call(call.person_ptr())

    @classmethod
    def un_hide_body(cls):
        if cls.map_data.get_stat() == 3:
            # 透明call
            logger.info("关闭透明 {}", 2)
            call.hide_call(call.person_ptr())

    @classmethod
    def follow_monster_switch(cls):
        # 跟随怪物
        if config().getint("自动配置", "跟随打怪") == 1:
            while True:
                cls.traversal.follow_monster()

    @classmethod
    def pick_item(cls):
        # 捡物品
        cls.pick.pickup()

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
                if cls.map_data.is_dialog_esc():
                    helper.key_press_release('esc')
                    helper.key_press_release('space')
                    continue
                if cls.map_data.is_dialog_esc() and (cls.map_data.is_dialog_a() and cls.map_data.is_dialog_b()):
                    helper.key_press_release('esc')
                    helper.key_press_release('space')
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
                    # 第一个房间 加buff
                    if cls.firstEnterMap is True and cls.addBuff is False:
                        buff = config().get("自动配置", "buff技能")
                        skill.buff_key(buff)
                        cls.addBuff = True
                    if cls.firstEnterMap is False and cls.map_data.is_town() is False:
                        # 透明call
                        call.hide_call(call.person_ptr())
                        # sss评分
                        sss_score = config().getint("自动配置", "评分")
                        mem.write_long(mem.read_long(address.PFAddr) + address.CEPfAddr, sss_score)
                        # 无视建筑
                        # cls.traversal.ignore_building(True)
                        # 进图开启功能
                        # cls.start_func()
                        cls.firstEnterMap = True

                    # 跟随怪物
                    if config().getint("自动配置", "跟随打怪") == 1:
                        cls.traversal.follow_monster()

                    # boss房间 使用觉醒
                    if cls.map_data.is_boss_room():
                        if cls.map_data.is_pass() is False:
                            supper_skill_str = config().get("自动配置", "觉醒技能")
                            supper_skill_list = supper_skill_str.split(",")
                            skill.super_skill(supper_skill_list)

                    # 过图
                    if cls.map_data.is_open_door() is True and cls.map_data.is_boss_room() is False:
                        # 捡物品
                        cls.pick.pickup()
                        # 过图
                        cls.pass_map()
                        continue

                    # 通关
                    if cls.map_data.is_boss_room():
                        if cls.map_data.is_pass():
                            # 捡物品
                            cls.pick.pickup()
                            # 关闭功能
                            cls.start_func()
                            # 关闭穿透
                            # cls.traversal.ignore_building(False)
                            # 退出副本
                            cls.quit_map()
                            cls.firstEnterMap = False
                            cls.addBuff = False
            except Exception as err:
                print("-----------自动线程开始-----------")
                except_type, _, except_traceback = sys.exc_info()
                print(except_type)
                print(err.args)
                print(except_traceback)
                print('-----------')
                for i in traceback.extract_tb(except_traceback):
                    print(i)
                print("-----------自动线程结束-----------")

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

        role_name = cls.map_data.get_role_name()
        logger.info("进入角色 {} ".format(role_name), 2)
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
        check_fatigue = config().getint("自动配置", "预留疲劳")
        if cls.map_data.get_pl() <= check_fatigue:
            cls.return_role()
            return

        time.sleep(0.5)
        # 分解装备
        cls.equip.handle_equip()

        # 随机处理
        breaks = config().getint("自动配置", "休息次数")
        run_time.modulo_algorithm(cls.completedNum, breaks)

        # 1 剧情 2 搬砖
        auto_model = config().getint("自动配置", "自动模式")
        if auto_model == 1 and cls.map_data.get_role_level() < 110:
            init.global_data.map_id = cls.task.handle_main()
            init.global_data.map_level = 0
        if auto_model == 2 and cls.map_data.get_role_level() == 110:
            if cls.map_data.get_fame() < 23330:
                map_ids = list(map(int, config().get("自动配置", "普通地图").split(",")))
            else:
                map_ids = list(map(int, config().get("自动配置", "英豪地图").split(",")))

            random_number = random.randint(0, len(map_ids) - 1)
            init.global_data.map_id = map_ids[random_number]
            init.global_data.map_level = config().getint("自动配置", "地图难度")

        if init.global_data.map_id == 0:
            logger.info("地图编号为空,无法切换区域", 2)
            return

        time.sleep(0.2)
        # 区域发包
        call.area_call(init.global_data.map_id)

        time.sleep(0.2)
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
        """进图  这个5 会自动适配是否进图的  从高到低 没开图 自动开图 我说是下面那个case 选其他难度 1-4的时候 会卡住"""
        if map_level == 5:
            for i in range(4, -1, -1):
                if cls.map_data.get_stat() == 3:
                    break
                if cls.map_data.get_stat() == 2:
                    cls.pack.go_map(map_id, i, 0, 0)
                    time.sleep(1)
                if cls.map_data.get_stat() == 1:
                    cls.select_map()
        else:
            cls.pack.go_map(map_id, map_level, 0, 0)

        while cls.thread_switch:
            time.sleep(0.2)
            # 进图副本跳出循环
            stat = cls.map_data.get_stat()
            if stat == 3:
                break

    @classmethod
    def pass_map(cls):
        """过图"""
        if cls.map_data.is_open_door() is False or cls.map_data.is_boss_room() is True:
            return

        over_map = config().getint("自动配置", "过图方式")
        over_map_size = config().getint("自动配置", "卡门重试")
        random_wait = config().getint("自动配置", "过图等待")

        '''过图随机'''
        if random_wait != 0:
            time.sleep(random.uniform(0, random_wait))

        if over_map > 0:
            # 寻路过图
            map_data = cls.game_map.map_data()
            if len(map_data.map_route) >= 2:
                direction = cls.game_map.get_direction(map_data.map_route[0], map_data.map_route[1])
                if over_map == 1:
                    call.over_map_call(direction)
                if over_map == 2:
                    for i in range(over_map_size):
                        call.drift_over_map(direction)
                        time.sleep(0.5)
                    if cls.map_data.is_open_door() is True and cls.map_data.is_boss_room() is False:
                        logger.info("被卡门 强制过图", 1)
                        # call.over_map_call(direction)

    @classmethod
    def quit_map(cls):
        """出图"""
        cls.completedNum = cls.completedNum + 1
        logger.info("自动刷图 [ {} ] 剩余疲劳 [ {} ]".format(cls.completedNum, cls.map_data.get_pl()), 2)
        time.sleep(0.2)
        # 翻牌
        cls.pack.get_income(0, random.randint(0, 3))

        out_type = config().getint("自动配置", "出图方式")
        if out_type == 2:
            out_value = config().get("自动配置", "出图按键")
            for i in range(3):
                helper.key_press_release(out_value)
            if cls.map_data.get_stat() == 1 and cls.map_data.is_town():
                return

        if out_type == 0:
            time.sleep(5)

        cls.level_map_while()

    @classmethod
    def level_map_while(cls):
        while cls.thread_switch:
            time.sleep(0.2)
            # 出图
            cls.pack.leave_map()
            if cls.map_data.get_stat() == 1 or cls.map_data.is_town():
                break
