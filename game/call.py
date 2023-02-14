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
    if not run_status:
        return

    run_status = True
    hook_shell = address.HBCallAddr
    hook_shell = hook_shell + 144
    hook_jump = hook_shell + 19
    hook_data = mem.read_bytes(hook_shell, 19)
    hook_old_data = hook_data

    hook_data = hook_data + convert.add_bytes(hook_data, [72, 184], convert.int_to_bytes(jump_address, 8))
    hook_data = convert.add_bytes(hook_data, [131, 56, 1, 117, 42, 72, 129, 236, 0, 3, 0, 0])
    hook_data = convert.add_bytes(hook_data, [72, 187], convert.int_to_bytes(blank_address, 8))
    hook_data = convert.add_bytes(hook_data, [255, 211])
    hook_data = convert.add_bytes(hook_data, [72, 184], convert.int_to_bytes(blank_address, 8))
    hook_data = convert.add_bytes(hook_data, [199, 0, 3, 0, 0, 0])
    hook_data = convert.add_bytes(hook_data, [72, 129, 196, 0, 3, 0, 0])
    hook_data = convert.add_bytes(hook_data, [255, 37, 0, 0, 0, 0], convert.int_to_bytes(hook_jump, 8))

    if mem.read_int(assembly_transit) == 0:
        mem.write_bytes(assembly_transit, hook_data)

    mem.write_bytes(assembly_transit, convert.add_bytes(byte_arr, [195]))
    hook_shell_value = convert.add_list([255, 37, 0, 0, 0, 0], convert.int_to_bytes(assembly_transit, 8),
                                        [144, 144, 144, 144, 144])
    mem.write_bytes(hook_shell, bytes(hook_shell_value))
    mem.write_int(jump_address, 1)

    while mem.read_int(jump_address) == 1:
        time.sleep(20)

    mem.write_bytes(hook_shell, hook_old_data)
    mem.write_bytes(blank_address, convert.get_empty_bytes(len(byte_arr) + 16))
    run_status = False
