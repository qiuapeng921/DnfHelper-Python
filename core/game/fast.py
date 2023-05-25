import time

from common import helper


class FastCall:
    # 设置全局变量
    g_Hook接口 = None
    g_Call最大长度 = None
    g_RSP = None
    g_超时调用设置 = None
    g_分配空间 = None
    g_上次空间 = None
    g_挂钩地址 = None
    g_旧数据 = None
    g_旧数据保存 = None
    g_中转框架内存 = None
    g_执行函数代码段 = None
    g_执行函数result = None
    g_执行函数控制符 = None
    g_执行函数刷新Time = None
    g_执行函数上次Time = None
    g_执行函数数据段 = None
    g_hook框架段 = None
    全局_lock_tea = None

    mem = None

    def __init__(self, mem):
        self.mem = mem

    def allocate_space(self, length):
        """分配空间"""
        result = self.g_上次空间
        self.g_上次空间 = self.g_上次空间 + length
        return result

    def init_hook_type(self, interface_selection: int):
        self.g_旧数据保存 = self.allocate_space(8)
        if interface_selection == 1:
            hook_address = self.mem.read_long(123)  # TranslateMessage
            hook_address = hook_address + self.mem.read_int(hook_address + 2) + 6
            self.g_挂钩地址 = hook_address

        if self.mem.read_long(self.g_旧数据保存) == 0:
            self.g_旧数据 = self.mem.read_long(self.g_挂钩地址)
        else:
            self.g_旧数据 = self.mem.read_long(self.g_旧数据保存)

    def call_wait(self):
        """调用等待"""
        while self.mem.read_int(self.g_执行函数控制符) == 1:
            time.sleep(0.01)

        while self.mem.read_int(self.g_执行函数控制符) == 2:
            refresh_time = self.mem.read_int(self.g_执行函数刷新Time) - self.mem.read_int(self.g_执行函数上次Time)
            if self.g_超时调用设置 != 0 and refresh_time > self.g_超时调用设置:
                break
            time.sleep(0.01)

    def call_function_auto_find_stack(self, call_data: bytes, rsp: int = None) -> int:
        """调用函数_自动找堆栈"""
        if rsp is None:
            rsp = self.g_RSP
        if call_data[len(call_data)] == 195:
            call_data[len(call_data)] = 144

        call_data = [72, 129, 236]
        call_data = helper.add_list(call_data, helper.int_to_bytes(rsp, 4))
        call_data = helper.add_list(call_data, [72, 129, 196], helper.int_to_bytes(rsp, 4))

        return self.memory_compilation(bytes(call_data))

    def memory_compilation(self, call_data: bytes) -> int:
        """内存汇编"""
        self.call_wait()
        call_data = helper.add_list(list(call_data),[195])
        if len(call_data) > self.g_Call最大长度:
            # 信息框(调用数过长)
            return 0

        self.mem.write_bytes(self.g_执行函数数据段, call_data)
        self.mem.write_int(self.g_执行函数控制符, 1)
        self.call_wait()
        self.mem.write_bytes(self.g_执行函数数据段, helper.get_empty_bytes(len(call_data)))
        result = self.mem.read_long(self.g_执行函数result)
        return result

    def fast_call(self, func, *args) -> int:
        """远程调用call"""
        if len(args) > 16:
            return 0

        params_array = list()
        for i in range(len(args)):
            if args[i] is not None:
                params_array.append(args[i])

        instruction_array = [47432, 47688, 47177, 47433]

        code = list()
        for i in range(len(params_array)):
            index = len(params_array) - i + 1
            if index <= 4:
                code = helper.add_list(code, instruction_array[index], helper.int_to_bytes(params_array[index], 8))
            code = helper.add_list(code, [72, 184], helper.int_to_bytes(params_array[index], 8))
            code = helper.add_list(code, [72, 137, 132, 36], helper.int_to_bytes((index - 1) * 8, 4))

        code = helper.add_list(code, [72, 184], helper.int_to_bytes(func, 8), [255, 208])

        if len(params_array) < 4:
            rsp = 4 * 8 + 8
        else:
            rsp = len(params_array) * 8 + 8

        if rsp / 8 % 2 == 0:
            rsp = rsp + 8

        new_code = helper.add_list([], [72, 129, 236], helper.int_to_bytes(rsp, 4))
        new_code = helper.add_list(new_code, code, [72, 129, 196], helper.int_to_bytes(rsp, 4))
        return self.memory_compilation(bytes(new_code))
