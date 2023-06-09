# coding=gbk

import time
import ctypes


class KeyboardInputKi(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
        ('unused', ctypes.c_ubyte * 8)
    ]


class KeyboardInput(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ki", KeyboardInputKi)
    ]


def drive_button(vk_code: int, send_type: int, func_type: bool):
    """
    驱动按键
    按键码
    按键方式 0按下+抬起  1按下 2抬起
    功能键方式 true为长按
    :param vk_code: int
    :param send_type:int
    :param func_type: bool
    :return:
    """
    user32 = ctypes.windll.user32

    ki = KeyboardInputKi()
    ki.wVk = vk_code
    ki.wScan = user32.MapVirtualKeyW(vk_code, 0)
    ki.dwExtraInfo = ctypes.pointer(ctypes.c_ulong(0))

    if send_type == 0 or send_type == 1:
        ki.dwFlags = 1 if func_type else 0
        ki.time = int(time.time() * 1000)
        inp = KeyboardInput(type=1, ki=ki)
        user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))
    if send_type == 0 or send_type == 2:
        ki.dwFlags = 3 if func_type else 2
        ki.time = int(time.time() * 1000)
        inp = KeyboardInput(type=1, ki=ki)
        user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))


def get_key_state(key_code: int) -> bool:
    """
    按键状态
    :param key_code:
    :return:
    """
    user32 = ctypes.windll.user32
    get_key_state_api = user32.GetKeyState
    get_key_state_api.argtypes = [ctypes.c_int]
    get_key_state_api.restype = ctypes.c_short
    state = get_key_state_api(key_code)
    return state & 0x8000 != 0
