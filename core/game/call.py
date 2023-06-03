import time

import keyword
from common import helper
from core.game import mem, map_data
from core.game import init, address
from core.game import skill, init, address
from common import helper, logger
import win32gui
from core.game import mem, fast_call as fc
from core.game.addr import address_all

fast_call = fc.FastCall


def init_call():
    global fast_call
    fast_call = fc.FastCall(mem)
    fast_call.init_code()


# 是否执行完成
run_status = False


def compile_call(byte_arr: list):
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

    hook_data = helper.add_bytes(hook_data, [72, 184], helper.int_to_bytes(jump_address, 8))
    hook_data = helper.add_bytes(hook_data, [131, 56, 1, 117, 42, 72, 129, 236, 0, 3, 0, 0])
    hook_data = helper.add_bytes(hook_data, [72, 187], helper.int_to_bytes(blank_address, 8))
    hook_data = helper.add_bytes(hook_data, [255, 211])
    hook_data = helper.add_bytes(hook_data, [72, 184], helper.int_to_bytes(jump_address, 8))
    hook_data = helper.add_bytes(hook_data, [199, 0, 3, 0, 0, 0])
    hook_data = helper.add_bytes(hook_data, [72, 129, 196, 0, 3, 0, 0])
    hook_data = helper.add_bytes(hook_data, [255, 37, 0, 0, 0, 0], helper.int_to_bytes(hook_jump, 8))

    if mem.read_int(assembly_transit) == 0:
        mem.write_bytes(assembly_transit, hook_data)

    mem.write_bytes(blank_address, helper.add_bytes(bytes(byte_arr), [195]))
    hook_shell_value = helper.add_list([255, 37, 0, 0, 0, 0], helper.int_to_bytes(assembly_transit, 8),
                                       [144, 144, 144, 144, 144])

    mem.write_bytes(hook_shell, bytes(hook_shell_value))

    mem.write_int(jump_address, 1)
    while mem.read_int(jump_address) == 1:
        time.sleep(0.5)
    mem.write_bytes(hook_shell, hook_old_data)
    mem.write_bytes(blank_address, helper.get_empty_bytes(len(byte_arr) + 16))
    run_status = False


def sub_rsp(i):
    """
    :param i: int
    :return: [int]
    """
    if i > 127:
        return helper.add_list([72, 129, 236], helper.int_to_bytes(i, 4))
    return helper.add_list([72, 131, 236], [i])


def add_rsp(i):
    """
    :param i: int
    :return: [int]
    """
    if i > 127:
        return helper.add_list([72, 129, 196], helper.int_to_bytes(i, 4))
    return helper.add_list([72, 131, 196], [i])


def call(addr):
    """
    :param addr: int
    :return: [int]
    """
    shell_code = [255, 21, 2, 0, 0, 0, 235, 8]
    return helper.add_list(shell_code, helper.int_to_bytes(addr, 8))


def get_per_ptr_call(addr: int):
    """
    取人物指针Call
    :param addr:
    :return:
    """
    shell_code = helper.add_list(sub_rsp(100), call(address.RWCallAddr), [72, 163])
    shell_code = helper.add_list(shell_code, helper.int_to_bytes(addr, 8))
    shell_code = helper.add_list(shell_code, add_rsp(100))
    compile_call(shell_code)
    return mem.read_long(addr)


def person_ptr():
    """人物指针"""
    person_addr = get_per_ptr_call(address.RwKbAddr)
    if person_addr == 0 or person_addr is None:
        logger.info("人物指针获取失败, 直接退出程序", 1)
        exit(1)
    return person_addr


def skill_call_power_random(supper_skill_list):
    # 获取当前窗口的焦点
    title = helper.get_process_name()
    if title == "地下城与勇士：创新世纪":
        """技能call"""
        key = skill.pick_key()
        key.remove(supper_skill_list)
        helper.key_press_release_list(key)


def skill_call_power(un_used):
    # 获取当前窗口的焦点
    title = helper.get_process_name()
    if title == "地下城与勇士：创新世纪":
        """技能call"""
        helper.key_press("x")
        key = skill.skill_map_cool_down(un_used)
        helper.key_press_release(key)
        helper.key_release("x")


def skill_call(addr: int, code: int, harm: int, x: int, y: int, z: int, size: float):
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
    shell_code = helper.add_list(shell_code, [72, 185], helper.int_to_bytes(empty_addr, 8))
    shell_code = helper.add_list(shell_code, [72, 184], helper.int_to_bytes(address.JNCallAddr, 8))
    shell_code = helper.add_list(shell_code, [255, 208, 72, 129, 196, 0, 2, 0, 0])
    compile_call(shell_code)


def hide_call(obj_ptr: int):
    """透明call"""
    shell_code = [72, 129, 236, 0, 2, 0, 0]
    shell_code = helper.add_list(shell_code, [65, 191, 255, 255, 255, 255])
    shell_code = helper.add_list(shell_code, [199, 68, 36, 32, 255, 255, 0, 0])
    shell_code = helper.add_list(shell_code, [65, 185, 1, 0, 0, 0])
    shell_code = helper.add_list(shell_code, [73, 184, 1, 0, 0, 0, 0, 0, 0, 0])
    shell_code = helper.add_list(shell_code, [186, 1, 0, 0, 0])
    shell_code = helper.add_list(shell_code, [72, 185], helper.int_to_bytes(obj_ptr, 8))
    shell_code = helper.add_list(shell_code, [72, 184], helper.int_to_bytes(address.TmCallAddr, 8))
    shell_code = helper.add_list(shell_code, [255, 208, 72, 129, 196, 0, 2, 0, 0])
    compile_call(shell_code)


def drift_call(ptr, x, y, z, speed):
    """
    漂移call
    :param ptr: int
    :param x: int 目标地址
    :param y: int 目标地址
    :param z: int
    :param speed: int 速度
    :return:
    """
    shell_code = [72, 129, 236, 0, 8, 0, 0]
    shell_code = helper.add_list(shell_code, [185, 241, 0, 0, 0])
    shell_code = helper.add_list(shell_code, [72, 184], helper.int_to_bytes(address.SqNcCallAddr, 8))
    shell_code = helper.add_list(shell_code, [255, 208])
    shell_code = helper.add_list(shell_code, [72, 139, 240, 72, 139, 200])
    shell_code = helper.add_list(shell_code, [72, 184], helper.int_to_bytes(address.PyCall1Addr, 8))
    shell_code = helper.add_list(shell_code, [255, 208])
    shell_code = helper.add_list(shell_code, [185], helper.int_to_bytes(x, 4))
    shell_code = helper.add_list(shell_code, [137, 8])
    shell_code = helper.add_list(shell_code, [185], helper.int_to_bytes(y, 4))
    shell_code = helper.add_list(shell_code, [137, 72, 4])
    shell_code = helper.add_list(shell_code, [185], helper.int_to_bytes(z, 4))
    shell_code = helper.add_list(shell_code, [137, 72, 8, 72, 141, 72, 24])
    shell_code = helper.add_list(shell_code, [186], helper.int_to_bytes(speed, 4))
    shell_code = helper.add_list(shell_code, [72, 184], helper.int_to_bytes(address.PyCall2Addr, 8))
    shell_code = helper.add_list(shell_code, [255, 208])
    shell_code = helper.add_list(shell_code,
                                 [51, 219, 137, 95, 48, 199, 135, 224, 0, 0, 0, 2, 0, 0, 0, 72, 141, 69, 136, 72, 137,
                                  68, 36, 96, 72, 137, 93, 136, 72, 137, 93, 144, 51, 210, 72, 141, 77, 136])
    shell_code = helper.add_list(shell_code, [72, 184], helper.int_to_bytes(address.XrNcCallAddr, 8))
    shell_code = helper.add_list(shell_code, [72, 139, 206, 72, 139, 1])
    shell_code = helper.add_list(shell_code,
                                 [72, 139, 6, 137, 92, 36, 64, 72, 137, 92, 36, 56, 72, 137, 92, 36, 48, 137, 92, 36,
                                  40, 72, 141, 77, 136, 72, 137, 76, 36, 32, 69, 51, 201])
    shell_code = helper.add_list(shell_code, [72, 186], helper.int_to_bytes(ptr, 8))
    shell_code = helper.add_list(shell_code, [73, 184], helper.int_to_bytes(ptr, 8))
    shell_code = helper.add_list(shell_code, [72, 139, 206])
    shell_code = helper.add_list(shell_code, [255, 144], helper.int_to_bytes(312, 4))
    shell_code = helper.add_list(shell_code, [72, 129, 196, 0, 8, 0, 0])
    compile_call(shell_code)


def move_call(max_map, mix_map, x, y):
    """移动Call"""
    role_ptr = mem.read_long(address.JSPtrAddr)
    mem.write_int(address.CzSyRdxAddr, max_map)
    mem.write_int(address.CzSyRdxAddr + 4, mix_map)
    mem.write_int(address.CzSyRdxAddr + 8, x)
    mem.write_int(address.CzSyRdxAddr + 12, y)
    shell_code = helper.add_list(sub_rsp(256), [72, 186], helper.int_to_bytes(address.CzSyRdxAddr, 8))
    shell_code = helper.add_list(shell_code, [72, 185], helper.int_to_bytes(role_ptr, 8))
    shell_code = helper.add_list(shell_code, call(address.CzSyCallAddr))
    shell_code = helper.add_list(shell_code, add_rsp(256))
    compile_call(shell_code)


def area_call(map_num):
    """区域Call"""
    region_addr = mem.read_long(address.QyParamAddr)
    tmp_region_call = address.QyCallAddr
    shell_code = [72, 131, 236, 48]
    shell_code = helper.add_list(shell_code, helper.add_list([65, 184], helper.int_to_bytes(map_num, 4)))
    shell_code = helper.add_list(shell_code, [186, 174, 12, 0, 0])
    shell_code = helper.add_list(shell_code, [72, 184, 255, 255, 255, 255, 0, 0, 0, 0])
    shell_code = helper.add_list(shell_code, helper.add_list([72, 185], helper.int_to_bytes(address.QyParamAddr, 8)))
    shell_code = helper.add_list(shell_code, [72, 139, 9], [76, 139, 201, 73, 129, 193])
    shell_code = helper.add_list(shell_code, helper.int_to_bytes(address.QyPyAddr, 4), [73, 131, 233, 64])
    shell_code = helper.add_list(shell_code, helper.add_list([72, 184], helper.int_to_bytes(tmp_region_call, 8)))
    shell_code = helper.add_list(shell_code, [255, 208, 72, 131, 196, 48])
    compile_call(shell_code)
    max_region = mem.read_int(region_addr + address.QyPyAddr + 0)
    min_region = mem.read_int(region_addr + address.QyPyAddr + 4)
    town_x = mem.read_int(region_addr + address.QyPyAddr + 8)
    town_y = mem.read_int(region_addr + address.QyPyAddr + 12)
    return move_call(max_region, min_region, town_x, town_y)


def over_map_call(fx):
    """
    过图call
    :param fx: 0左 1右 2上 3下
    """
    if init.map_data.is_town():
        return
    if not init.map_data.is_open_door():
        return
    empty_addr = address.GtKbAddr
    room_data = mem.read_long(mem.read_long(mem.read_long(address.FJBHAddr) + address.SJAddr) + address.StPyAddr)
    shell_code = [65, 185, 255, 255, 255, 255]
    shell_code = helper.add_list(shell_code, [73, 184], helper.int_to_bytes(empty_addr, 8))
    shell_code = helper.add_list(shell_code, [186], helper.int_to_bytes(fx, 4))
    shell_code = helper.add_list(shell_code, [72, 185], helper.int_to_bytes(room_data, 8))
    shell_code = helper.add_list(shell_code, [72, 184], helper.int_to_bytes(address.GtCallAddr, 8))
    shell_code = helper.add_list(shell_code, [255, 208])
    compile_call(shell_code)


def drift_over_map(fx):
    """
    漂移顺图
    :param fx: 0左 1右 2上 3下
    """
    if init.map_data.is_town():
        return
    if not init.map_data.is_open_door():
        return

    addr = person_ptr()
    map_offset = mem.read_long(addr + address.DtPyAddr)
    if map_offset == 0:
        return

    room_data = mem.read_long(mem.read_long(mem.read_long(address.FJBHAddr) + address.SJAddr) + address.StPyAddr)
    coordinate_structure = room_data + fx * address.FxIdAddr + address.ZbStPyAddr
    start_x = mem.read_int(coordinate_structure + 0)
    start_y = mem.read_int(coordinate_structure + 4)
    end_x = mem.read_int(coordinate_structure + 8)
    end_y = mem.read_int(coordinate_structure + 12)
    x, y = (int(0), int(0))
    if fx == 0:
        # 左
        x = int(start_x + end_x + 20)
        y = int(start_y + end_y / 2)

    if fx == 1:
        # 右
        x = int(start_x - 20)
        y = int(start_y + end_y / 2)
    if fx == 2:
        # 上
        x = int(start_x + end_x / 2)
        y = int(start_y + end_y + 20)
    if fx == 3:
        # 下
        x = int(start_x + end_x / 2)
        y = int(start_y - 20)

    drift_call(addr, x, y, 0, 50)
    time.sleep(0.1)
    drift_call(addr, int(start_x + end_x / 2), start_y, 0, 50)


def jump_over_task_call():
    # 跳过任务Call
    shell_code = sub_rsp(512)
    shell_code = helper.add_list(shell_code, [65, 131, 201, 255])
    shell_code = helper.add_list(shell_code, [69, 9, 200])
    shell_code = helper.add_list(shell_code, [186, 1, 0, 0, 0])
    shell_code = helper.add_list(shell_code, [72, 185], helper.int_to_bytes(address.TaskAddr, 8))
    shell_code = helper.add_list(shell_code, [72, 139, 9])
    shell_code = helper.add_list(shell_code, call(address.TgCallAddr))
    shell_code = helper.add_list(shell_code, add_rsp(512))
    compile_call(shell_code)


def accept_task_call(task_id):
    # 接受任务Call
    shell_code = sub_rsp(40)
    helper.add_list(shell_code, [186], helper.int_to_bytes(task_id, 4))
    helper.add_list(shell_code, call(address.JsCallAddr))
    helper.add_list(shell_code, add_rsp(40))
    compile_call(shell_code)


def finish_task_call(task_id):
    # 完成任务Call
    shell_code = sub_rsp(512)
    helper.add_list(shell_code, [179, 255])
    helper.add_list(shell_code, [68, 15, 182, 203])
    helper.add_list(shell_code, [65, 176, 255])
    helper.add_list(shell_code, [186], helper.int_to_bytes(task_id, 4))
    helper.add_list(shell_code, call(address.WcCallAddr))
    helper.add_list(shell_code, add_rsp(512))
    compile_call(shell_code)


def submit_task_call(task_id):
    # 提交任务Call
    shell_code = sub_rsp(48)
    helper.add_list(shell_code, [65, 189, 1, 0, 0, 0])
    helper.add_list(shell_code, [65, 190, 255, 255, 255, 255])
    helper.add_list(shell_code, [69, 139, 205])
    helper.add_list(shell_code, [69, 139, 198])
    helper.add_list(shell_code, [72, 185], helper.int_to_bytes(address.TaskAddr, 8))
    helper.add_list(shell_code, [72, 139, 9])
    helper.add_list(shell_code, [186], helper.int_to_bytes(task_id, 4))
    helper.add_list(shell_code, call(address.TjCallAddr))
    helper.add_list(shell_code, add_rsp(48))
    compile_call(shell_code)


def skill_down_call(skill_addr):
    if skill_addr > 0:
        empty_addr = address.CoolDownKbAddr
        mem.write_int(empty_addr, 0)
        shell_code = [72, 131, 236, 32]
        helper.add_list(shell_code, [49, 210])
        helper.add_list(shell_code, [72, 185], helper.int_to_bytes(skill_addr, 8))
        helper.add_list(shell_code, [255, 21, 2, 0, 0, 0, 235, 8])
        helper.add_list(shell_code, helper.int_to_bytes(address_all.冷却判断CALL, 8))
        helper.add_list(shell_code, [72, 162], helper.int_to_bytes(address.CoolDownKbAddr, 8))
        helper.add_list(shell_code, [72, 131, 196, 32])
        compile_call(shell_code)
        return mem.read_int(empty_addr) < 0
    else:
        return False


def cool_down_call(skill_addr):
    if skill_addr < 0:
        return False
    empty_addr = address.CoolDownKbAddr
    mem.write_int(empty_addr, 0)
    shell_code = [72, 131, 236, 32]
    helper.add_list(shell_code, [49, 210])
    helper.add_list(shell_code, [72, 185], helper.int_to_bytes(skill_addr, 8))
    helper.add_list(shell_code, [255, 21, 2, 0, 0, 0, 235, 8])
    helper.add_list(shell_code, helper.int_to_bytes(address.LqCallJudgeAddr, 8))
    helper.add_list(shell_code, [72, 162], helper.int_to_bytes(empty_addr, 8))
    helper.add_list(shell_code, [72, 131, 196, 32])
    compile_call(shell_code)
    return mem.read_int(empty_addr) < 1


# 移动技能
def skill_move(skill_index, skill_empty):
    try:
        fast_call.call(address.JnYdCallAddr, address.JnlAddr(), person_ptr(), skill_index, skill_empty)
    except Exception as e:
        logger.file("read_longlong 技能位置:{},移动位置:{},错误:{}".format(skill_index, skill_index, e.args))


# 技能三无
def skill_nothing():
    # dw.WriteByteArr(game.JnSwAddr, []byte{144, 144, 144, 144, 144})
    mem.write_bytes(address_all.技能三无, [144, 144, 144, 144, 144])
