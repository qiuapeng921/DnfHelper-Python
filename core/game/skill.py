import time
import random
from enum import Enum

from common import helper, logger
from core.game import address, call, fast_call
from core.game import mem, map_data
from core.game.addr import address_all, xiaochen_address


class Skill:
    @classmethod
    def __init__(cls):
        pass


class KeyCode(Enum):
    VK_A = 'a'
    VK_S = 's'
    VK_D = 'd'
    VK_F = 'f'
    VK_G = 'g'
    VK_H = 'h'
    VK_X = 'x'
    VK_Q = 'q'
    VK_W = 'w'
    VK_E = 'e'
    VK_R = 'r'
    VK_T = 't'
    VK_Y = 'y'
    VK_TAB = 'tab'
    VK_ALT = 'alt'
    VK_CTRL = 'ctrl'


# 技能列表
strings = ['z', 'c', 'v', 'a', 's', 'd', 'f', 'g', 'h', 'w', 'e', 'r', 't', 'y']
# 权重
weights = [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# 不好用的技能
un_use = ['流心', '后跳', '属性变换', '受身蹲伏', '刀魂', '三段刃', '流心', '格林机枪', '锁魂刺']


def buff_key(buff):
    if helper.is_dnf_win():
        helper.key_press_release(buff)


# 觉醒技能
def super_skill(super_skill_list):
    if strings.__contains__(super_skill_list):
        strings.remove(super_skill_list)

    if helper.is_dnf_win():
        helper.key_press_release(super_skill_list)


'''解密1 ＝ 读整数型 (技能指针 ＋ #判断冷却1)
解密2 ＝ 读整数型 (技能指针 ＋ #判断冷却2)
解密3 ＝ _float (读整数型 (技能指针 ＋ #判断冷却3))
ret ＝ 读整数型 (#冷却参数_1 ＋ 读整数型 (#冷却参数_2 ＋ 16) × #冷却判断偏移3) ＋ 读整数型 (#冷却参数_2 ＋ 24)
ret ＝ 到整数 (到小数 (ret － 解密2) × 解密3 ＋ 到小数 (解密2))
返回 (选择 (ret － 解密1 ＞ 0, 0, 解密1 － ret))'''


def check_skill_down(skill_addr) -> str:
    # 解密1 ＝ 读整数型 (技能指针 ＋ #判断冷却1)
    jnl_address_1 = mem.read_int(skill_addr + address_all.浮点冷却)
    # 解密2 ＝ 读整数型 (技能指针 ＋ #判断冷却2)
    jnl_address_2 = mem.read_int(skill_addr + xiaochen_address.判断冷却_2)
    # 解密3 ＝ _float (读整数型 (技能指针 ＋ #判断冷却3))
    jnl_address_3 = float(mem.read_int(skill_addr + xiaochen_address.判断冷却_3))

    # ret ＝ 读整数型 (#冷却参数_1 ＋ 读整数型 (#冷却参数_2 ＋ 16) × #冷却判断偏移3) ＋ 读整数型 (#冷却参数_2 ＋ 24)
    ret = mem.read_int(
        xiaochen_address.冷却参数_1 + mem.read_int(xiaochen_address.冷却参数_2 + 16) * 4) + mem.read_int(
        xiaochen_address.冷却参数_2 + 24)
    # ret ＝ 到整数 (到小数 (ret － 解密2) × 解密3 ＋ 到小数 (解密2))
    ret = int(float(ret - jnl_address_2) * jnl_address_3 + float(jnl_address_2))
    # 返回 (选择 (ret － 解密1 ＞ 0, 0, 解密1 － ret))
    return 0 if ret - jnl_address_1 > 0 else jnl_address_1 - ret


def skill_name_map():
    skill_ptr = get_skill_base_addr()
    skill_map = {}
    for i in range(14):
        skill_str = mem.read_long(skill_ptr + i * 24 + 16) - 16
        if skill_str is None or skill_str < 0:
            continue
        # 技能名称
        name = get_skill_name(skill_str)
        # 技能等级
        skill_item_level_ptr = mem.read_int(skill_str + address.JnDjAddr)
        skill_map[skill_str] = name

    return skill_map


def skill_map():
    skill_ptr = get_skill_base_addr()
    skill_map = {}
    for i in range(14):
        skill_str = mem.read_long(skill_ptr + i * 24 + 16) - 16
        if skill_str is None:
            continue
        check_skill_down(skill_str)
        print(get_skill_name(skill_str))

    return skill_map


def get_skill_base_addr():
    rw_addr = call.person_ptr()
    # 技能栏
    jnl_address = mem.read_long(rw_addr + address.JnlAddr)
    # 技能栏偏移
    skill_ptr = mem.read_long(jnl_address + address.JnlPyAddr)
    return skill_ptr


# 获取技能名称
def get_skill_name(skill_addr):
    skill_name_addr = mem.read_long(skill_addr + address.JnMcAddr)
    if skill_name_addr is None:
        return ""
    name_bytes = mem.read_bytes(skill_name_addr, 200)
    return helper.unicode_to_ascii(name_bytes)


# 技能空位
def empty_skill() -> int:
    for i in range(408):
        a = i - 1
        temp = mem.read_long(get_skill_base_addr() + a * 8)
        if mem.read_int(temp) == 0:
            if a > 13:
                return a


# 移动技能
def skill_move(skill_index, skill_empty):
    try:
        call.fast_call.call(address.JnYdCallAddr, address.JnlAddr(), call.person_ptr(), skill_index, skill_empty)
    except Exception as e:
        logger.file("read_longlong 技能位置:{},移动位置:{},错误:{}".format(skill_index, skill_index, e.args))


# 移除掉不好用的技能
def remove_skill():
    skill_data = skill_name_map()
    if len(skill_data) < 0:
        return
    for index, key in enumerate(skill_data.keys()):
        print(index, key, skill_data[key])
        if un_use.__contains__(skill_data[key]):
            # 存在不好用的技能
            skill_move(index - 1, empty_skill())


#  循环技能冷却
def select_skill_cool_down() -> str:
    # 读取技能栏
    skill_data = skill_name_map()
    if len(skill_data) < 0:
        return KeyCode.VK_X.value
    for index, key in enumerate(skill_data.keys()):
        print(index, key, skill_data[key])
        code = KeyCode.VK_X
        if key > 0 and call.is_cooling_call(key):
            if index == 0:
                code = KeyCode.VK_A
            elif index == 1:
                code = KeyCode.VK_S
            elif index == 2:
                code = KeyCode.VK_D
            elif index == 3:
                code = KeyCode.VK_F
            elif index == 4:
                code = KeyCode.VK_G
            elif index == 5:
                code = KeyCode.VK_H
            elif index == 6:
                code = KeyCode.VK_X
            elif index == 7:
                code = KeyCode.VK_Q
            elif index == 8:
                code = KeyCode.VK_W
            elif index == 9:
                code = KeyCode.VK_E
            elif index == 10:
                code = KeyCode.VK_R
            elif index == 11:
                code = KeyCode.VK_T
            elif index == 12:
                code = KeyCode.VK_Y
            elif index == 13:
                code = KeyCode.VK_TAB
            return code.value
        return code.value


def pick_strings(keys, num_picks, weights_temp):
    if len(keys) != len(weights_temp):
        raise ValueError("Length of strings and weights must be the same")
    if num_picks > len(keys):
        raise ValueError("Number of picks cannot be greater than the length of strings")

    # Calculate the cumulative sum of weights
    cum_weights = [0] * len(weights_temp)
    cum_weights[0] = weights_temp[0]
    for i in range(1, len(weights_temp)):
        cum_weights[i] = cum_weights[i - 1] + weights_temp[i]

    # Generate a list of random numbers between 0 and the total weight
    total_weight = cum_weights[-1]
    rand_nums = [random.randint(0, total_weight - 1) for _ in range(num_picks)]

    # Pick the strings based on the random numbers
    picks = []
    for rand_num in rand_nums:
        for i in range(len(cum_weights)):
            if rand_num < cum_weights[i]:
                picks.append(keys[i])
                break

    return picks


def pick_key(num_picks: int = 5):
    return pick_strings(strings, num_picks, weights)


'''以下是读取内存方法'''


# 取剩余SP值
def get_sp():
    # mem.read_long (mem.read_long (mem.read_long (#技能SP值) ＋ #技能SP值一级) ＋ #技能SP值二级)
    return mem.read_long(
        mem.read_long(mem.read_long(address_all.技能SP值) + address_all.技能SP值一级) + address_all.技能SP值二级)


# 技能冷却判断
def check_skill_down_single(key):
    skill_addr = get_skill_base_addr()

    result = 0
    if key == KeyCode.VK_A.value:
        result = mem.read_long(skill_addr + address_all.技能A)
    elif key == KeyCode.VK_S.value:
        result = mem.read_long(skill_addr + address_all.技能S)
    elif key == KeyCode.VK_D.value:
        result = mem.read_long(skill_addr + address_all.技能D)
    elif key == KeyCode.VK_F.value:
        result = mem.read_long(skill_addr + address_all.技能F)
    elif key == KeyCode.VK_G.value:
        result = mem.read_long(skill_addr + address_all.技能G)
    elif key == KeyCode.VK_H.value:
        result = mem.read_long(skill_addr + address_all.技能H)
    elif key == KeyCode.VK_ALT.value:
        result = mem.read_long(skill_addr + address_all.技能Alt)
    elif key == KeyCode.VK_Q.value:
        result = mem.read_long(skill_addr + address_all.技能Q)
    elif key == KeyCode.VK_W.value:
        result = mem.read_long(skill_addr + address_all.技能W)
    elif key == KeyCode.VK_E.value:
        result = mem.read_long(skill_addr + address_all.技能E)
    elif key == KeyCode.VK_R.value:
        result = mem.read_long(skill_addr + address_all.技能R)
    elif key == KeyCode.VK_T.value:
        result = mem.read_long(skill_addr + address_all.技能T)
    elif key == KeyCode.VK_Y.value:
        result = mem.read_long(skill_addr + address_all.技能Y)
    elif key == KeyCode.VK_CTRL.value:
        result = mem.read_long(skill_addr + address_all.技能Ctrl)

    result = mem.read_long(result + 16) - 16
    if result == 0 or result is None:
        return 1
    skill_name = get_skill_name(result)
    if skill_name == "":
        return 1

    return call.is_cooling_call(result)


if __name__ == '__main__':
    # 使用pick_strings方法进行随机选择
    picks = pick_strings(strings, 5, weights)
    print(picks)

    while True:
        picks = pick_key(5)
        time.sleep(0.5)
        print(picks)
