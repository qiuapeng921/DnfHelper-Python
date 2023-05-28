import time
import random
from enum import Enum

from common import helper
from core.game import address, call
from core.game import mem, map_data


def check_skill_down(skill_addr) -> str:
    temp_addr = skill_addr
    jnl_address_1 = mem.read_long(temp_addr + address.JnlQAddr1)
    jnl_address_2 = mem.read_long(temp_addr + address.JnlQAddr2)
    jnl_address_3 = mem.read_float(temp_addr + address.JnlQAddr3)

    ret = mem.read_long(
        address.JnLqCs1 + mem.read_long(address.JnLqCs2 + 16) * address.JnLqPd3) + mem.read_long(
        address.JnLqCs2 + 24)
    ret = int(ret - jnl_address_2 * jnl_address_3) + jnl_address_2
    print(ret)
    return ret - jnl_address_1 if ret - jnl_address_1 > 0 else jnl_address_1 - ret


def skill_name():
    rw_addr = call.person_ptr()
    # 技能栏
    jnl_address = mem.read_long(rw_addr + address.JnlAddr)
    # 技能栏偏移
    skill_ptr = mem.read_long(jnl_address + address.JnlPyAddr)
    skill_map = {}
    for i in range(14):
        skill_str = mem.read_long(mem.read_long(skill_ptr + i * 24) + 16) - 16
        # 技能名称
        skill_item_name_ptr = mem.read_long(skill_str + address.JnMcAddr)
        name = helper.address_to_str(skill_item_name_ptr)
        # 技能等级
        skill_item_level_ptr = helper.address_to_int(skill_str + address.JnDjAddr)
        skill_map[skill_str] = name

    return skill_map


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


# 重新构建strings和weights
# 后续可以读技能名称处理
strings = ['z', 'c', 'v', 'a', 's', 'd', 'f', 'g', 'h', 'w', 'e', 'r', 't', 'y']

weights = [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


def buff_key(buff):
    title = helper.get_process_name()
    if title == "地下城与勇士：创新世纪":
        helper.key_press_release(buff)


def super_skill(super_skill_list):
    title = helper.get_process_name()
    if title == "地下城与勇士：创新世纪":
        helper.key_press_release(super_skill_list)

    if strings.__contains__(super_skill_list):
        strings.remove(super_skill_list)


#  循环技能冷却
def skill_cool_down() -> str:
    skill_data = skill_name()
    if len(skill_data) < 0:
        return KeyCode.VK_X.value
    for index, key in enumerate(skill_data.keys()):
        print(index, key, skill_data[key])
        code = KeyCode.VK_X
        if key > 0 and check_skill_down(key):
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
            return KeyCode.VK_X.value
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


if __name__ == '__main__':
    # 使用pick_strings方法进行随机选择
    picks = pick_strings(strings, 5, weights)
    print(picks)

    while True:
        picks = pick_key(5)
        time.sleep(0.5)
        print(picks)
