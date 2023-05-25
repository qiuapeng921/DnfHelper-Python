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

    def 分配空间(self, 分配长度):
        result = self.g_上次空间
        self.g_上次空间 = self.g_上次空间 + 分配长度
        return result

    def InitHookType(self, 接口选择: int):
        self.g_旧数据保存 = self.分配空间(8)
        if 接口选择 == 1:
            挂钩地址 = self.mem.read_long(123)  # TranslateMessage
            挂钩地址 = 挂钩地址 + self.mem.read_int(挂钩地址 + 2) + 6
            self.g_挂钩地址 = 挂钩地址

        if self.mem.read_long(self.g_旧数据保存) == 0:
            self.g_旧数据 = self.mem.read_long(self.g_挂钩地址)
        else:
            self.g_旧数据 = self.mem.read_long(self.g_旧数据保存)

    def 调用等待(self):
        while self.mem.read_int(self.g_执行函数控制符) == 1:
            time.sleep(0.01)

        while self.mem.read_int(self.g_执行函数控制符) == 2:
            刷新时间 = self.mem.read_int(self.g_执行函数刷新Time) - self.mem.read_int(self.g_执行函数上次Time)
            if self.g_超时调用设置 != 0 and 刷新时间 > self.g_超时调用设置:
                break
            time.sleep(0.01)

    def 调用函数_自动找堆栈(self, 调用数据: bytes, rsp: int = None) -> int:
        if rsp is None:
            rsp = self.g_RSP
        if 调用数据[len(调用数据)] == 195:
            调用数据[len(调用数据)] == 144

        调用数据 = [72, 129, 236]
        调用数据 = helper.add_list(调用数据, helper.int_to_bytes(rsp, 4))
        调用数据 = helper.add_list(调用数据, [72, 129, 196], helper.int_to_bytes(rsp, 4))

        return self.内存汇编1(调用数据)

    def 内存汇编1(self, 调用数据: bytes) -> int:
        self.调用等待()
        调用数据 = 调用数据 + {195}
        if len(调用数据) > self.g_Call最大长度:
            # 信息框(调用数过长)
            return 0

        self.mem.write_bytes(self.g_执行函数数据段, 调用数据)
        self.mem.write_int(self.g_执行函数控制符, 1)
        self.调用等待()
        self.mem.write_bytes(self.g_执行函数数据段, helper.get_empty_bytes(len(调用数据)))
        result = self.mem.read_long(self.g_执行函数result)
        tuple
        return result

    def FastCall(self, func, *args) -> int:
        if len(args) > 16:
            return 0

        参数数组 = []
        for i in range(len(args)):
            if args[i] is not None:
                参数数组.append(args[i])

        指令集 = [47432, 47688, 47177, 47433]

        code = []
        for i in range(len(参数数组)):
            index = len(参数数组) - i + 1
            if index <= 4:
                code = helper.add_list(code, 指令集[index], helper.int_to_bytes(参数数组[index], 8))
            code = helper.add_list(code, [72, 184], helper.int_to_bytes(参数数组[index], 8))
            code = helper.add_list(code, [72, 137, 132, 36], helper.int_to_bytes((index - 1) * 8, 4))

        code = helper.add_list(code, [72, 184], helper.int_to_bytes(func, 8), [255, 208])

        if len(参数数组) < 4:
            rsp = 4 * 8 + 8
        else:
            rsp = len(参数数组) * 8 + 8

        if rsp / 8 % 2 == 0:
            rsp = rsp + 8

        new_code = helper.add_list([], [72, 129, 236], helper.int_to_bytes(rsp, 4))
        new_code = helper.add_list(new_code, code, [72, 129, 196], helper.int_to_bytes(rsp, 4))
        return (self.内存汇编1(new_code))
