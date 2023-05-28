import random
import time
import random
from enum import Enum

from common import helper
from core.game import address, call


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

def skill_name(mem) -> str:
    rw_addr = call.person_ptr()
    # 技能栏
    jnl_address = mem.read_long(rw_addr + address.JnlAddr)
    # 技能栏偏移
    skill_ptr = mem.read_long(jnl_address + address.JnlPyAddr)

    for i in range(13):
        # 技能栏循环
        skill_name_long = mem.read_long(skill_ptr + i * 16)
        if skill_name_long == 0 or skill_name_long is None:
            continue
        # 技能栏名称
        skill_name_addr = mem.read_long(skill_name_long + address.JnMcAddr)
        if skill_name_addr == 0 or skill_name_addr is None:
            continue
        # 读字节
        name_bytes = mem.read_bytes(skill_name_addr, 400)
        if name_bytes is not None:
            # 转unicode
            skill_name = helper.unicode_to_ascii(name_bytes)
            # print(skill_name)


#  循环技能冷却
def skill_cool_down(mem) -> str:
    rw_addr = call.person_ptr()
    # 技能栏
    jnl_address = mem.read_long(rw_addr + address.JnlAddr)
    # 技能栏偏移
    skill_ptr = mem.read_long(jnl_address + address.JnlPyAddr)

    code = KeyCode.VK_X
    for i in range(1, 15):
        temp_skill_addr = mem.read_long(skill_ptr + i * 16)
        if temp_skill_addr > 0 and call.cool_down_call(temp_skill_addr):
            if i == 0:
                code = KeyCode.VK_A
            elif i == 1:
                code = KeyCode.VK_S
            elif i == 2:
                code = KeyCode.VK_D
            elif i == 3:
                code = KeyCode.VK_F
            elif i == 4:
                code = KeyCode.VK_G
            elif i == 5:
                code = KeyCode.VK_H
            elif i == 6:
                code = KeyCode.VK_X
            elif i == 7:
                code = KeyCode.VK_Q
            elif i == 8:
                code = KeyCode.VK_W
            elif i == 9:
                code = KeyCode.VK_E
            elif i == 10:
                code = KeyCode.VK_R
            elif i == 11:
                code = KeyCode.VK_T
            elif i == 12:
                code = KeyCode.VK_Y
            elif i == 13:
                code = KeyCode.VK_X
            return code.value
    return code.value


def pick_strings(keys, num_picks, weights):
    if len(keys) != len(weights):
        raise ValueError("Length of strings and weights must be the same")
    if num_picks > len(keys):
        raise ValueError("Number of picks cannot be greater than the length of strings")

    # Calculate the cumulative sum of weights
    cum_weights = [0] * len(weights)
    cum_weights[0] = weights[0]
    for i in range(1, len(weights)):
        cum_weights[i] = cum_weights[i - 1] + weights[i]

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
        print(picks);
