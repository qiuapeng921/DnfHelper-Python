import time

from common import convert, mem
from game import address

# 是否执行完成
run_status = False


def compile_call(byte_arr: bytes):
    # 汇编中转, 空白地址, 跳转地址
    assembly_transit = address.NcBhKbAddr + 300
    blank_address = address.NcBhKbAddr + 500
    jump_address = blank_address - 100
    global run_status
    if run_status:
        return

    run_status = True
    hook_shell = address.HBCallAddr
    hook_shell = hook_shell + 144
    hook_jump = hook_shell + 19
    hook_data = mem.read_bytes(hook_shell, 19)
    hook_old_data = hook_data
    print(hook_data, list(hook_data))

    hook_data = convert.add_bytes(hook_data, [72, 184], convert.int_to_bytes(jump_address, 8))
    hook_data = convert.add_bytes(hook_data, [131, 56, 1, 117, 42, 72, 129, 236, 0, 3, 0, 0])
    hook_data = convert.add_bytes(hook_data, [72, 187], convert.int_to_bytes(blank_address, 8))
    hook_data = convert.add_bytes(hook_data, [255, 211])
    hook_data = convert.add_bytes(hook_data, [72, 184], convert.int_to_bytes(blank_address, 8))
    hook_data = convert.add_bytes(hook_data, [199, 0, 3, 0, 0, 0])
    hook_data = convert.add_bytes(hook_data, [72, 129, 196, 0, 3, 0, 0])
    hook_data = convert.add_bytes(hook_data, [255, 37, 0, 0, 0, 0], convert.int_to_bytes(hook_jump, 8))
    print(hook_data, list(hook_data))

    if mem.read_int(assembly_transit) == 0:
        mem.write_bytes(assembly_transit, hook_data)

    mem.write_bytes(assembly_transit, convert.add_bytes(byte_arr, [195]))
    hook_shell_value = convert.add_list([255, 37, 0, 0, 0, 0], convert.int_to_bytes(assembly_transit, 8),
                                        [144, 144, 144, 144, 144])

    print(hook_shell_value, list(hook_shell_value))
    mem.write_bytes(hook_shell, bytes(hook_shell_value))
    mem.write_int(jump_address, 1)

    while mem.read_int(jump_address) == 1:
        time.sleep(0.2)

    mem.write_bytes(hook_shell, hook_old_data)
    mem.write_bytes(blank_address, convert.get_empty_bytes(len(byte_arr) + 16))
    run_status = False


def sub_rsp(i):
    """
    :param i: int
    :return: [int]
    """
    if i > 127:
        return convert.add_list([72, 129, 236], convert.int_to_bytes(i, 4))
    return convert.add_list([72, 131, 236]).append(i)


def add_rsp(i):
    """
    :param i: int
    :return: [int]
    """
    if i > 127:
        return convert.add_list([72, 129, 196], convert.int_to_bytes(i, 4))
    return convert.add_list([72, 131, 196]).append(i)


def call(addr):
    """
    :param addr: int
    :return: [int]
    """
    shell_code = [255, 21, 2, 0, 0, 0, 235, 8]
    return convert.add_list(shell_code, convert.int_to_bytes(addr, 8))


def get_per_ptr_call(addr: int):
    """
    取人物指针Call
    :param addr:
    :return:
    """
    shell_code = convert.add_list([100], [address.RWCallAddr], [72, 163])
    shell_code = convert.add_list(shell_code, convert.int_to_bytes(addr, 8))
    shell_code = convert.add_list(shell_code, [100])
    compile_call(bytes(shell_code))
    return mem.read_int(addr)


def person_ptr():
    """人物指针"""
    return get_per_ptr_call(address.RwKbAddr)


def skill_call(addr, code, harm, x, y, z, size):
    """
    技能call
    :param addr:int 触发地址
    :param code:int 技能代码
    :param harm:int 技能伤害
    :param x:int
    :param y:int
    :param z:int
    :param size: float 技能大小
    :return:
    """
    empty_addr = address.JnKbAddr
    mem.write_long(empty_addr, addr)
    mem.write_int(empty_addr + 16, code)
    mem.write_int(empty_addr + 20, harm)
    mem.write_int(empty_addr + 32, x)
    mem.write_int(empty_addr + 36, y)
    mem.write_int(empty_addr + 40, z)
    mem.write_float(empty_addr + 140, size)
    mem.write_int(empty_addr + 144, 65535)
    mem.write_int(empty_addr + 148, 65535)
    shell_code = [72, 129, 236, 0, 2, 0, 0]
    shell_code = convert.add_list(shell_code, [72, 185], convert.int_to_bytes(empty_addr, 8))
    shell_code = convert.add_list(shell_code, [72, 184], convert.int_to_bytes(address.JNCallAddr, 8))
    shell_code = convert.add_list(shell_code, [255, 208, 72, 129, 196, 0, 2, 0, 0])
    compile_call(bytes(shell_code))


def hide_call(obj_ptr: int):
    """透明call"""
    shell_code = [72, 129, 236, 0, 2, 0, 0]
    shell_code = convert.add_list(shell_code, [65, 191, 255, 255, 255, 255])
    shell_code = convert.add_list(shell_code, [199, 68, 36, 32, 255, 255, 0, 0])
    shell_code = convert.add_list(shell_code, [65, 185, 1, 0, 0, 0])
    shell_code = convert.add_list(shell_code, [73, 184, 1, 0, 0, 0, 0, 0, 0, 0])
    shell_code = convert.add_list(shell_code, [186, 1, 0, 0, 0])
    shell_code = convert.add_list(shell_code, [72, 185], convert.int_to_bytes(obj_ptr, 8))
    shell_code = convert.add_list(shell_code, [72, 184], convert.int_to_bytes(address.TmCallAddr, 8))
    shell_code = convert.add_list(shell_code, [255, 208, 72, 129, 196, 0, 2, 0, 0])
    compile_call(bytes(shell_code))
