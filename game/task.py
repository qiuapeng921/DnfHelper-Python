import time

from typing import Tuple

from common import helper, logger
from game import init, address, call


class Task:
    def __init__(self, mem, pack, map_data):
        #  无任务刷新角色
        self.refreshTask = False
        self.mem = mem
        self.pack = pack
        self.map_data = map_data

    def handle_main(self):
        """
        处理主线
        :return:
        """
        map_id = 0
        next_task_id = 0

        # 提交主线
        self.submit_task()
        while init.global_data.auto_switch:
            time.sleep(0.3)
            task_name, task_condition, task_id = self.main_line_task()
            # 处理相同任务输出
            if task_id != next_task_id and task_id > 0:
                next_task_id = task_id
                logger.info("主线任务->任务名称 {}".format(task_name), 1)
                # logger.info("主线任务->任务条件 {}".format(task_condition), 1)
                # logger.info("主线任务->任务ID {}".format(task_id), 1)

            # 无任务,刷新角色
            if task_id == 0:
                if not self.refreshTask:
                    time.sleep(0.2)
                    logger.info("暂无任务或卡任务,重新选择角色", 1)
                    self.pack.return_role()
                    time.sleep(2)
                    self.pack.select_role(init.global_data.completed_role)
                    time.sleep(0.5)
                    self.refreshTask = True
                    continue
                else:
                    map_id = self.highest_map()
                    logger.info("暂无任务,执行适应等级地图", 1)
                    return map_id

            self.refreshTask = False

            # 跳过部分无法完成任务，取最高等级执行
            # 任务名称[返回赫顿玛尔],任务条件[[seek n meet npc]],任务ID[3509] 材料不足无法完成任务
            # 任务名称[黑市的商人],任务条件[[seek n meet npc]],任务ID[5943] 蛇肉任务
            task_ids = [3509, 5943]
            if task_id in task_ids:
                map_id = self.highest_map()
                logger.info("无法完成任务,执行适应等级地图", 1)
                return map_id

            #  是否可以跳过任务
            #  86级寂静城任务无法跳过 任务id{3850, 3851, 3858, 3859, 3860, 3861, 3864, 3865, 3866, 3867, 3868}
            ok, task_level = self.can_skip(task_id)
            if ok and task_level not in [85, 86]:
                # 跳过任务
                call.jump_over_task_call()
                continue

            # 任务未接，执行接取任务
            if self.finish_status(task_id) == -1:
                # self.pack.accept_task(task_id)
                call.accept_task_call(task_id)

            #  任务完成，执行提交任务
            if self.finish_status(task_id) == 0:
                # self.pack.submit_task(task_id)
                call.submit_task_call(task_id)
                continue

            # 剧情条件判断
            if self.conditional(task_condition) == 1:
                # self.pack.finish_task(task_id)
                call.finish_task_call(task_id)

            # 刷图任务
            if self.conditional(task_condition) == 2:
                map_id = self.task_map(task_id)
                if map_id > 0:
                    return map_id

            # 材料任务
            if self.conditional(task_condition) == 3:
                map_id = self.highest_map()
                logger.info("材料任务无法自动完成,执行最高等级地图", 1)
                return map_id

        return map_id

    def main_line_task(self) -> Tuple[str, str, int]:
        mem = self.mem
        task_addr = mem.read_long(address.TaskAddr)
        start = mem.read_long(task_addr + address.QbRwStartAddr)
        end = mem.read_long(task_addr + address.QbRwEndAddr)
        num = int((end - start) / 8)

        for i in range(num):
            task_ptr = mem.read_long(start + i * 8)
            task_type = mem.read_int(task_ptr + address.RwLxAddr)
            if task_type == 0:
                task_length = mem.read_int(task_ptr + address.RwDxAddr)
                if task_length > 7:
                    tmp = mem.read_long(task_ptr + 16)
                    task_name_byte = list(mem.read_bytes(tmp, 100))
                    task_name = helper.unicode_to_ascii(task_name_byte)
                else:
                    task_name_byte = list(mem.read_bytes(task_ptr + 16, 100))
                    task_name = helper.unicode_to_ascii(task_name_byte)
                # 任务条件
                task_conditional = helper.unicode_to_ascii(
                    list(mem.read_bytes(mem.read_long(task_ptr + address.RwTjAddr), 100)))
                # 任务编号
                task_id = mem.read_int(task_ptr)
                return task_name, task_conditional, task_id

        return "", "", 0

    def can_skip(self, task_id) -> [bool, int]:
        """是否跳过"""
        mem = self.mem
        task_addr = mem.read_long(address.TaskAddr)
        start = mem.read_long(task_addr + address.YjRwStartAddr)
        end = mem.read_long(task_addr + address.YjRwEndAddr)
        num = int((end - start) / 16)

        for i in range(num):
            task_ptr = mem.read_long(start + i * 16)
            if mem.read_int(task_ptr) == task_id:
                task_level = mem.read_int(task_ptr + address.RwDjAddr)
                if task_level < self.map_data.get_role_level():
                    return True, task_level

        return False, 0

    def conditional(self, conditional) -> int:
        """
            conditional_judgment 条件判断
            1=城镇完成 比如：对话任务   2=刷图任务，需要进图  3=材料任务
        """
        brush_conditions = [
            "[meet npc]",
            "[seek n meet npc]",
            "[reach the range]",
            "[look cinematic]",
            "[question]",
            "[quest clear]",
        ]
        if conditional in brush_conditions:
            return 1

        brush_conditions = [
            "[hunt monster]",
            "[hunt enemy]",
            "[condition under clear]",
            "[clear map]",
            "[question]",
            "[seeking]",
            "[clear dungeon index]",
        ]
        if conditional in brush_conditions:
            return 2

        return 0

    def task_map(self, task_id: int) -> int:
        """任务地图"""
        mem = self.mem
        task_addr = mem.read_long(address.TaskAddr)
        start = mem.read_long(task_addr + address.YjRwStartAddr)
        end = mem.read_long(task_addr + address.YjRwEndAddr)
        num = int((end - start) / 16)

        for i in range(num):
            task_ptr = mem.read_long(start + i * 16)
            if mem.read_int(task_ptr) == task_id:
                task_data = mem.read_long(task_ptr + address.RwFbAddr)
                return mem.read_int(task_data)
        return 0

    def submit_task(self):
        """提交任务"""
        mem = self.mem
        task_addr = mem.read_long(address.TaskAddr)
        start = mem.read_long(task_addr + address.QbRwStartAddr)
        end = mem.read_long(task_addr + address.QbRwEndAddr)
        num = int((end - start) / 8)

        for i in range(num):
            task_ptr = mem.read_long(start + i * 8)
            task_type = mem.read_int(task_ptr + address.RwLxAddr)
            if task_type == 0:
                task_id = mem.read_int(task_ptr)
                # self.pack.submit_task(task_id)
                call.submit_task_call(task_id)

        start = mem.read_long(task_addr + address.YjRwStartAddr)
        end = mem.read_long(task_addr + address.YjRwEndAddr)
        num = int((end - start) / 16)
        for i in range(num):
            task_ptr = mem.read_long(start + i * 16)
            task_type = mem.read_int(task_ptr + address.RwLxAddr)
            if task_type == 0:
                task_id = mem.read_int(task_ptr)
                # self.pack.submit_task(task_id)
                call.submit_task_call(task_id)

    def finish_status(self, task_id: int):
        """
        完成状态
        -1 任务未接  0 任务完成 1 已接任务
        """
        mem = self.mem
        task_addr = mem.read_long(address.TaskAddr)
        start = mem.read_long(task_addr + address.YjRwStartAddr)
        end = mem.read_long(task_addr + address.YjRwEndAddr)
        num = int((end - start) / 16)

        tmp_arr = []
        for i in range(num):
            pointer = mem.read_long(start + i * 16)
            if mem.read_int(pointer) == task_id:
                frequency = self.map_data.decode(start + i * 16 + 8)
                if frequency < 512:
                    return frequency
                elif frequency == 512:
                    return 1

                tmp_arr[0] = int(frequency % 512)
                the_rest = int(frequency) - tmp_arr[0]
                if the_rest < 262144:
                    tmp_arr[1] = int(the_rest / 512)
                    tmp_arr[1] = int(the_rest % 262144 / 512)
                the_rest = int(the_rest - tmp_arr[0] * 512)
                if the_rest < 262144:
                    tmp_arr[2] = 0
                    tmp_arr[2] = int(the_rest % 262144)
                # 数组排序 从大到小
                tmp_arr.sort(reverse=True)
                if tmp_arr[0] == 0:
                    tmp_arr[0] = 1
                return tmp_arr[0]
        return -1

    def highest_map(self):
        """最高等级"""
        role_level = self.map_data.get_role_level()
        if role_level <= 17:
            if role_level <= 3:
                return 3  # 雷鸣废墟
            if role_level <= 5:
                return 5  # 雷鸣废墟
            if role_level <= 8:
                return 6  # 猛毒雷鸣废墟
            if role_level <= 11:
                return 9  # 冰霜幽暗密林
            if role_level <= 13:
                return 7  # 格拉卡
            if role_level <= 15:
                return 8  # 烈焰格拉卡
            if role_level <= 17:
                return 1000  # 暗黑雷鸣废墟
            return 0

        # 天空之城
        if role_level <= 23:
            if role_level <= 18:
                return 1000  # 10 龙人之塔
            if role_level <= 19:
                return 12  # 人偶玄关
            if role_level <= 20:
                return 13  # 石巨人塔
            if role_level <= 21:
                return 14  # 黑暗玄廊
            if role_level <= 22:
                return 17  # 悬空城
            if role_level <= 23:
                return 15  # 城主宫殿
            return 0

        # 神殿脊椎
        if role_level <= 29:
            if role_level <= 24:
                return 15  # 21 神殿外围
            if role_level <= 25:
                return 22  # 树精丛林
            if role_level <= 26:
                return 23  # 炼狱
            if role_level <= 27:
                return 24  # 极昼
            if role_level <= 28:
                return 25  # 第一脊椎
            if role_level <= 29:
                return 26  # 第二脊椎
            return 0

        # 暗精灵地区
        if role_level <= 35:
            if role_level <= 30:
                return 26  # 31  浅栖之地
            if role_level <= 31:
                return 32  # 蜘蛛洞穴
            if role_level <= 32:
                return 150  # 蜘蛛王国
            if role_level <= 33:
                return 151  # 英雄冢
            if role_level <= 34:
                return 35  # 暗精灵墓地
            if role_level <= 35:
                return 34  # 熔岩穴
            return 0

        # 祭坛
        if role_level <= 39:
            if role_level <= 36:
                return 34  # 152 暴君的祭坛
            if role_level <= 37:
                return 153  # 黄金矿洞
            if role_level <= 38:
                return 154  # 远古墓穴深处
            if role_level <= 39:
                return 154  # 远古墓穴深处
            return 0

        # 雪山
        if role_level <= 45:
            if role_level <= 40:
                return 154  # 40 山脊
            if role_level <= 41:
                return 41  # 冰心少年
            if role_level <= 42:
                return 42  # 利库天井
            if role_level <= 44:
                return 141  # 布万加的修炼场
            if role_level <= 45:
                return 141  # 布万加的修炼场
            return 0

        # 绿都
        if role_level <= 49:
            if role_level <= 46:
                return 141  # 61  绿都格罗兹尼
            if role_level <= 47:
                return 50  # 堕落的盗贼
            if role_level <= 48:
                return 51  # 迷乱之村哈穆林
            if role_level <= 49:
                return 53  # 疑惑之村
            return 0

        if role_level <= 53:
            if role_level <= 50:
                return 53  # 144  炽晶森林
            if role_level <= 51:
                return 145  # 冰晶森林
            if role_level <= 52:
                return 146  # 水晶矿脉
            if role_level <= 53:
                return 148  # 幽冥监狱
            return 0

        if role_level <= 58:
            if role_level <= 54:
                return 148  # 156 蘑菇庄园
            if role_level <= 55:
                return 157  # 蚁后的巢穴
            if role_level <= 56:
                return 158  # 腐烂之地
            if role_level <= 57:
                return 159  # 赫顿玛尔旧街区
            if role_level <= 58:
                return 160  # 鲨鱼栖息地
            return 0

        if role_level <= 62:
            if role_level <= 59:
                return 160  # 162  '人鱼国度
            if role_level <= 60:
                return 163  # GBL女神殿
            if role_level <= 61:
                return 164  # 树精繁殖地
            if role_level <= 62:
                return 164  # 树精繁殖地
            return 0

        if role_level <= 70:
            if role_level <= 63:
                return 164  # 80  '根特外围
            if role_level <= 64:
                return 81  # 根特东门
            if role_level <= 65:
                return 82  # 根特南门
            if role_level <= 66:
                return 88  # 根特北门
            if role_level <= 67:
                return 88  # 根特北门
            if role_level <= 68:
                return 83  # 夜间袭击战
            if role_level <= 69:
                return 84  # 补给阻断站
            if role_level <= 70:
                return 85  # 追击歼灭战
            return 0

        # 海上列车
        if role_level <= 74:
            if role_level <= 71:
                return 85  # 86 列车上的海贼
            if role_level <= 71:
                return 87  # 夺回西部线
            if role_level <= 73:
                return 92  # 雾都赫伊斯
            if role_level <= 74:
                return 93  # 阿登高地
            return 0

        if role_level <= 80:
            if role_level <= 75:
                return 93  # 70 格兰之火
            if role_level <= 76:
                return 71  # 瘟疫之源
            if role_level <= 77:
                return 72  # 卡勒特之刃
            if role_level <= 78:
                return 74  # 绝密区域
            if role_level <= 79:
                return 75  # 昔日悲鸣
            if role_level <= 80:
                return 76  # 凛冬
            return 0

        if role_level <= 85:
            if role_level <= 81:
                return 76  # 102 普鲁兹发电站
            if role_level <= 82:
                return 103  # 特伦斯发电站
            if role_level <= 85:
                return 104  # 格蓝迪发电站
            return 0

        if role_level <= 86:
            return 192  # 钢铁之臂
        if role_level <= 90:
            if role_level <= 87:
                return 310  # 时间广场
            if role_level <= 88:
                return 312  # 恐怖的栖息地
            if role_level <= 89:
                return 314  # 红色魔女之森
            if role_level <= 90:
                return 314  # 红色魔女之森
            return 0

        if role_level <= 100:
            if role_level <= 95:
                return 291100293  # 全蚀市场
            if role_level <= 98:
                return 291100293  # 搏击俱乐部

        if role_level <= 109:
            if role_level <= 100:
                return 100002975  # 圣域外围
            if role_level <= 102:
                return 100002976  # 圣域中心
            if role_level <= 103:
                return 100002977  # 泽尔峡谷
            if role_level <= 104:
                return 100002978  # 洛仑山
            if role_level <= 105:
                return 100002979  # 白色雪原
            if role_level <= 106:
                return 100002980  # 贝奇的空间
            if role_level <= 107:
                return 100002981
            if role_level <= 108:
                return 100002982
            if role_level <= 109:
                return 100002983

        return 0
