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
    hook_data = mem.ReadBytes(hook_shell, 19)
    hook_old_data = hook_data

    hook_data = hook_data + convert.AddBytes(hook_data, [72, 184], convert.IntToBytes(jump_address, 8))
    hook_data = convert.AddBytes(hook_data, [131, 56, 1, 117, 42, 72, 129, 236, 0, 3, 0, 0])

    hook_data = convert.AddBytes(hook_data, [72, 187], convert.IntToBytes(kbDz, 8))
    hook_data = convert.AddBytes(hook_data, [255, 211])
    hook_data = convert.AddBytes(hook_data, [72, 184], convert.IntToBytes(pdDz, 8))
    hook_data = convert.AddBytes(hook_data, [199, 0, 3, 0, 0, 0])
    hook_data = convert.AddBytes(hook_data, [72, 129, 196, 0, 3, 0, 0])
    hook_data = convert.AddBytes(hook_data, [255, 37, 0, 0, 0, 0], convert.IntToBytes(hook_jump, 8))

    if mem.ReadInt(assembly_transit) == 0:
        mem.WriteBytes(hbZz, hook_data)

    mem.WriteBytes(kbDz, convert.AddBytes(paramsShellCode, [195]))
    hook_shell_value = convert.AddList([255, 37, 0, 0, 0, 0], convert.IntToBytes(assembly_transit, 8),
                                       [144, 144, 144, 144, 144])
    mem.WriteBytes(HookShell, bytes(hook_shell_value))
    mem.WriteInt(pdDz, 1)

    while mem.ReadInt(pdDz) == 1:
        time.sleep(20)

    mem.WriteBytes(hook_shell, hook_old_data)
    mem.WriteBytes(blank_address, convert.GetEmptyBytes(len(byte_arr) + 16))
    run_status = False
