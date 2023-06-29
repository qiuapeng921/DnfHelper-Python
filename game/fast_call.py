import time

from common import helper
from game import address


class FastCall:
    g_hook_interface = None
    g_call_max_len = None
    g_RSP = None
    g_timeout_call_settings = None
    g_allocate_space = None
    g_last_space = None
    g_hook_address = None
    g_old_data = None
    g_old_data_save = None
    g_transit_framework_memory = None
    g_execute_func_code = None
    g_execute_func_result = None
    g_execute_func_control = None
    g_execute_func_refresh_time = None
    g_execute_func_last_time = None
    g_execute_func_data = None
    g_hook_framework = None

    mem = None

    def __init__(self, mem):
        self.mem = mem

    def init_code(self):
        self.g_hook_interface = 1
        self.g_call_max_len = 6666
        self.g_RSP = 584
        self.g_allocate_space = self.mem.allocate(4906 * 1024)
        self.g_timeout_call_settings = 1000 * 60
        self.g_last_space = self.g_allocate_space

        code = [72, 137, 116, 36, 8, 72, 137, 124, 36, 16, 65, 86, 72, 131, 236, 32, 72, 190, 0, 0, 0, 64, 1, 0, 0, 0,
                72, 191, 118, 11, 204, 63, 1, 0, 0, 0, 73, 190, 126, 11, 204, 63, 1, 0, 0, 0, 255, 214, 72, 163, 142,
                11, 204, 63, 1, 0, 0, 0, 131, 63, 1, 117, 57, 73, 199, 6, 0, 0, 0, 0, 72, 199, 7, 2, 0, 0, 0, 255, 214,
                72, 163, 134, 11, 204, 63, 1, 0, 0, 0, 65, 86, 87, 83, 86, 72, 184, 0, 0, 0, 80, 1, 0, 0, 0, 255, 208,
                94, 91, 95, 65, 94, 73, 137, 6, 199, 7, 0, 0, 0, 0, 72, 139, 116, 36, 48, 72, 139, 124, 36, 56, 72, 131,
                196, 32, 65, 94, 195]

        self.g_execute_func_code = self.allocate_space(len(code))
        self.g_execute_func_data = self.allocate_space(self.g_call_max_len)
        self.g_execute_func_control = self.allocate_space(8)
        self.g_execute_func_refresh_time = self.allocate_space(8)
        self.g_execute_func_result = self.allocate_space(8)
        self.g_execute_func_last_time = self.allocate_space(8)

        self.mem.write_bytes(self.g_execute_func_code, bytes(code))
        self.mem.write_long(self.g_execute_func_code + 0x10 + 2, self.mem.read_long(address.GameTimeGetTime))
        self.mem.write_long(self.g_execute_func_code + 0x1A + 2, self.g_execute_func_control)
        self.mem.write_long(self.g_execute_func_code + 0x24 + 2, self.g_execute_func_result)
        self.mem.write_long(self.g_execute_func_code + 0x30 + 2, self.g_execute_func_refresh_time)
        self.mem.write_long(self.g_execute_func_code + 0x4F + 2, self.g_execute_func_last_time)
        self.mem.write_long(self.g_execute_func_code + 0x5E + 2, self.g_execute_func_data)

        code = [72, 137, 92, 36, 8, 72, 137, 116, 36, 16, 87, 72, 131, 236, 32]
        code = helper.add_list(code, [72, 184], helper.int_to_bytes(self.g_execute_func_code, 8), [255, 208])
        code = helper.add_list(code, [72, 139, 92, 36, 48, 72, 139, 116, 36, 56, 72, 131, 196, 32, 95, 195])
        self.g_transit_framework_memory = self.allocate_space(len(code))
        self.mem.write_bytes(self.g_transit_framework_memory, bytes(code))
        self.init_hook_type(self.g_hook_interface)

        code = [80, 83, 81, 82, 87, 86, 85, 65, 80, 65, 81, 65, 82, 65, 83, 65, 84, 65, 85, 65, 86, 65, 87, 156, 72,
                131, 236, 40]
        code = helper.add_list(code, [72, 184], helper.int_to_bytes(self.g_transit_framework_memory, 8), [255, 208])
        code = helper.add_list(code,
                               [72, 131, 196, 40, 157, 65, 95, 65, 94, 65, 93, 65, 92, 65, 91, 65, 90, 65, 89, 65, 88,
                                93, 94, 95, 90, 89, 91, 88])
        code = helper.add_list(code, [255, 37, 0, 0, 0, 0], helper.int_to_bytes(self.g_old_data, 8))

        self.g_hook_framework = self.allocate_space(len(code))

        self.mem.write_bytes(self.g_hook_framework, bytes(code))
        self.mem.write_long(self.g_old_data_save, self.g_old_data)
        self.mem.write_long(self.g_hook_address, self.g_hook_framework)

    def free_code(self):
        """释放内存"""
        self.mem.write_long(self.g_hook_address, self.g_old_data)
        self.mem.write_bytes(self.g_transit_framework_memory,
                             helper.get_empty_bytes(self.g_last_space - self.g_allocate_space))

    def allocate_space(self, length):
        """分配空间"""
        result = self.g_last_space
        self.g_last_space = self.g_last_space + length
        return result

    def init_hook_type(self, interface_selection: int):
        self.g_old_data_save = self.allocate_space(8)
        if interface_selection == 1:
            hook_address = self.mem.read_long(address.TranslateMessage)
            hook_address = hook_address + self.mem.read_int(hook_address + 2) + 6
            self.g_hook_address = hook_address

        if self.mem.read_long(self.g_old_data_save) == 0:
            self.g_old_data = self.mem.read_long(self.g_hook_address)
        else:
            self.g_old_data = self.mem.read_long(self.g_old_data_save)

    def call_wait(self):
        """调用等待"""
        while self.mem.read_int(self.g_execute_func_control) == 1:
            time.sleep(0.001)

        while self.mem.read_int(self.g_execute_func_control) == 2:
            refresh_time = self.mem.read_int(self.g_execute_func_refresh_time) - self.mem.read_int(
                self.g_execute_func_last_time)
            if self.g_timeout_call_settings != 0 and refresh_time > self.g_timeout_call_settings:
                break
            time.sleep(0.001)

    def call_function_auto_find_stack(self, call_data: list, rsp: int = None) -> int:
        """调用函数_自动找堆栈"""
        if rsp is None:
            rsp = self.g_RSP
        if call_data[-1] == 195:
            call_data[-1] = 144

        call_data = helper.add_list([72, 129, 236], helper.int_to_bytes(rsp, 4), call_data, [72, 129, 196],
                                    helper.int_to_bytes(rsp, 4))

        return self.memory_compilation(call_data)

    def memory_compilation(self, call_data: list) -> int:
        """内存汇编"""
        self.call_wait()
        call_data = helper.add_list(call_data, [195])
        if len(call_data) > self.g_call_max_len:
            helper.message_box("调用数过长")
            return 0

        self.mem.write_bytes(self.g_execute_func_data, bytes(call_data))
        self.mem.write_int(self.g_execute_func_control, 1)
        self.call_wait()
        self.mem.write_bytes(self.g_execute_func_data, helper.get_empty_bytes(len(call_data)))
        result = self.mem.read_long(self.g_execute_func_result)
        return result

    def call(self, func, *args) -> int:
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
            if i < 4:
                code = helper.add_list(code, helper.int_to_bytes(instruction_array[i], 2))
                code = helper.add_list(code, helper.int_to_bytes(params_array[i], 8))
            else:
                code = helper.add_list(code, [72, 184], helper.int_to_bytes(params_array[i], 8))
                code = helper.add_list(code, [72, 137, 132, 36], helper.int_to_bytes(i * 8, 4))

        code = helper.add_list(code, [72, 184], helper.int_to_bytes(func, 8), [255, 208])

        if len(params_array) < 4:
            rsp = 4 * 8 + 8
        else:
            rsp = len(params_array) * 8 + 8

        if rsp / 8 % 2 == 0:
            rsp = rsp + 8

        code = helper.add_list([72, 129, 236], helper.int_to_bytes(rsp, 4), code, [72, 129, 196],
                               helper.int_to_bytes(rsp, 4))

        return self.memory_compilation(code)
