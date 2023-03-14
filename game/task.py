import time

from game import address, init


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
            if task_id != next_task_id:
                next_task_id = task_id
                # logging.Console.Printf("主线任务 -> 任务名称[%s],任务条件[%s],任务ID[%d] \n", taskName, taskCondition, taskId)

            # 无任务,刷新角色
            if task_id == 0:
                if not self.refreshTask:
                    time.sleep(0.2)
                    # logging.Console.Println("暂无任务或卡任务,重新选择角色")
                    # ZbFhJs()
                    time.sleep(2)
                    # ZbXzJs(completedRoleNum)
                    time.sleep(0.5)
                    self.refreshTask = True
                    continue
                else:
                    map_id = 104
                    # logging.Console.Println("暂无任务,执行适应等级地图")
                    break

            self.refreshTask = False
            #  是否可以跳过任务 // 86级寂静城任务无法跳过 任务id{3850, 3851, 3858, 3859, 3860, 3861, 3864, 3865, 3866, 3867, 3868}
            # ok, taskLevel := u.CanSkip(taskId)
            # if ok && !common.InArray[uint32](taskLevel, []uint32{85, 86}) {
            #     JumpOverTaskCall(taskId)
            #     continue
            # }

            # 任务未接，执行接取任务
            if self.finish_status(task_id) == -1:
                self.pack.accept_task(task_id)

            # 跳过部分无法完成任务，取最高等级执行
            # 任务名称[返回赫顿玛尔],任务条件[[seek n meet npc]],任务ID[3509] 材料不足无法完成任务
            # 任务名称[黑市的商人],任务条件[[seek n meet npc]],任务ID[5943] 蛇肉任务
            task_ids = [3509, 5943]
            if task_id in task_ids:
                map_id = 104  # u.HighestMap()
                # logging.Console.Println("无法完成任务,执行适应等级地图")
                break

            #  任务完成，执行提交任务
            if self.finish_status(task_id) == 0:
                self.pack.submit_task(task_id)
                continue

            # 剧情条件判断
            if self.conditional_judgment(task_condition) == 1:
                self.pack.finish_task(task_id)

            # 刷图任务
            if self.conditional_judgment(task_condition) == 2:
                map_id = self.task_map(task_id)
                if map_id > 0:
                    break

            if self.conditional_judgment(task_condition) == 3:
                pass
                # logging.Console.Println("材料任务无法自动完成,执行最高等级地图")

        return map_id

    def main_line_task(self) -> tuple[str, str, int]:
        mem = self.mem
        task_addr = mem.read_int(address.TaskAddr)
        start = mem.read_int(task_addr + address.QbRwStartAddr)
        end = mem.read_int(task_addr + address.QbRwEndAddr)
        num = int((end - start) / 8)

        for i in range(num):
            task_ptr = mem.read_long(start + i * 8)
            task_type = mem.read_int(task_ptr + address.RwLxAddr)
            if task_type == 0:
                task_length = mem.read_int(task_ptr + address.RwDxAddr)
                if task_length == 7:
                    # todo taskName = common.UnicodeToString(common.ReadByteArr(common.ReadInt64(taskPtr+16), 100))
                    task_name = mem.read_bytes(mem.read_long(task_ptr + 16), 100)
                else:
                    # todo taskName = common.UnicodeToString(common.ReadByteArr(taskPtr+16, 100))
                    task_name = mem.read_bytes(task_ptr + 16, 100)
                # todo common.UnicodeToString(common.ReadByteArr(common.ReadInt64(taskPtr+RwTjAddr), 100))
                # 任务条件
                task_conditional = mem.read_bytes(mem.read_long(task_ptr + address.RwTjAddr), 100)
                # 任务编号
                task_id = mem.read_int(task_ptr)
                return task_name, task_conditional, task_id

    def conditional_judgment(self, conditional) -> int:
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
        for i in range(len(brush_conditions)):
            if brush_conditions[i] == conditional:
                return 1

        brush_conditions = [
            "[hunt monster]",
            "[hunt enemy]",
            "[condition under clear]",
            "[clear map]",
            "[question]",
            "[seeking]",
        ]
        for i in range(len(brush_conditions)):
            if brush_conditions[i] == conditional:
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
                self.pack.submit_task(mem.read_int(task_ptr))

        start = mem.read_long(task_addr + address.YjRwStartAddr)
        end = mem.read_long(task_addr + address.YjRwEndAddr)
        num = int((end - start) / 16)
        for i in range(num):
            task_ptr = mem.read_long(start + i * 16)
            task_type = mem.read_int(task_ptr + address.RwLxAddr)
            if task_type == 0:
                self.pack.submit_task(mem.read_int(task_ptr))

    def finish_status(self, task_id: int):
        """
        完成状态
        -1 任务未接  0 任务完成 1 已接任务
        """
        mem = self.mem
        task_addr = mem.read_long(address.RwFbAddr)
        start = mem.read_long(task_addr + address.YjRwStartAddr)
        end = mem.read_long(task_addr + address.YjRwEndAddr)
        num = int((end - start) / 16)

        for i in range(num):
            pointer = mem.read_long(start + i * 16)
            if mem.read_int(pointer) == task_id:
                number = self.map_data.decode(start + i * 16 + 8)
                if number < 512:
                    return number
                elif number == 512:
                    return 1
                cnum = number % 512
                if cnum == 0:
                    return 1
                else:
                    return cnum
        return -1
