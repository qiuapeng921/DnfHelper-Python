from common import memory
from common.helper import array_rand
from plugins.driver.keyboard import *

mem = memory.Memory()


def rand_skill() -> int:
    code = [
        VK_A, VK_S, VK_D, VK_F, VK_G, VK_H,
        VK_Q, VK_W, VK_E, VK_R, VK_T, VK_Y,
    ]
    return array_rand(code)
