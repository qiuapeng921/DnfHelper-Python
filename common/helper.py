import math
import struct
import threading
import time
from datetime import datetime

import keyboard
import psutil
import win32api
import win32gui
import random


def is_dnf_win():
    title = get_process_name()
    return title == "地下城与勇士：创新世纪"


def get_process_name():
    # 获取当前活动窗口句柄
    hwnd = win32gui.GetForegroundWindow()

    # 获取窗口标题
    window_title = win32gui.GetWindowText(hwnd)

    return window_title


def get_process_id_by_name(name: str) -> int:
    pid = 0
    ps = psutil.process_iter()
    for p in ps:
        if p.name() == name:
            pid = p.pid
            break

    return pid


def get_module_handle(pid: int, name: str) -> int:
    """
    获取模块句柄
    :param pid: 进程id
    :param name: 模块名称
    :return:
    """
    process = psutil.Process(pid)
    # 获取进程的所有模块句柄
    modules = process.memory_maps()
    # 遍历所有模块句柄并打印
    for module in modules:
        module_name = module.path.split("\\")
        if module_name[3] == name:
            return module.rss


sys_start_time = datetime.now()  # 记录程序启动时间


def get_app_run_time():
    """返回程序运行时间的格式化字符串"""
    current_time = datetime.now()  # 获取当前时间
    duration = current_time - sys_start_time  # 计算时间差

    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)

    # 格式化时间字符串
    time_string = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    return time_string


def get_now_date():
    """
    get_now_date 获取系统当前日期
    :return:  string
    """
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time


def int_to_bytes(int_val, int_type):
    """
    int转bytes
        :param int_val: int
        :param int_type:
        :return: bytes
    """
    if int_type == 2:
        return struct.pack('<H', int_val)
    if int_type == 4:
        return struct.pack('<I', int_val)
    if int_type == 8:
        return struct.pack('<Q', int_val)


def float_to_bytes(float_val, float_type):
    """
    float转bytes
    :param float_val: float
    :param float_type: int
    :return: bytes
    """
    if float_val == 4:
        return struct.pack('<f', float_type)
    if float_val == 8:
        return struct.pack('<d', float_type)


def add_bytes(old_bytes: bytes, *new_bytes_arr):
    """
    追加bytes
    :param old_bytes:
    :param new_bytes_arr:
    :return: bytes
    Example: add_byte(b'\x83\x84', [236, 0, 1, 0, 0], [1, 2, 3, 4]) -> b'\x83\x84\xec\x00\x01\x00\x00\x01\x02\x03\x04'
    """
    ret_bytes = add_list(list(old_bytes), *new_bytes_arr)
    return bytes(ret_bytes)


def add_list(old_list: list, *new_list_arr: list) -> list:
    """
    追加list
    :param old_list: list
    :param new_list_arr:
    :return: bytes
    # Example: add_byte([72], [129], [236, 0, 1, 0, 0], [1, 2, 3, 4]) -> [72, 129, 236, 0, 1, 0, 0, 1, 2, 3, 4]
    """
    if len(new_list_arr) == 0:
        return old_list
    for list_arr in new_list_arr:
        old_list += list_arr
    return old_list


def get_empty_bytes(count: int) -> bytes:
    result = list()
    for i in range(count):
        result.append(0)

    return bytes(result)


def message_box(msg):
    win32api.MessageBoxEx(0, msg, "Helper")


def ascii_to_unicode(string: str) -> list:
    bytes_arr = bytes()
    for c in string:
        hex_int = ord(c)
        bytes_arr = bytes_arr + hex_int.to_bytes(2, byteorder='little')

    return list(bytes_arr)


def unicode_to_ascii(ls: list) -> str:
    if isinstance(ls, bytes):
        ls = list(ls)

    text = ""
    for i in range(0, len(ls), 2):
        if ls[i] == 0 and ls[i + 1] == 0:
            break
        a = ls[i + 1] << 8
        b = ls[i]
        text += chr(a + b)

    return text


# 计算距离
def distance(x1, y1, x2, y2) -> float:
    # 距离 ＝ 求平方根 (求次方 (x1 － x2, 2) ＋ 求次方 (y1 － y2, 2))
    return abs(math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2)))


def key_press(key: str):
    keyboard.press(key)


def key_release(key: str):
    keyboard.release(key)


def key_press_release_with_delay(key: str, delay: float):
    keyboard.press(key)
    time.sleep(delay)
    keyboard.release(key)


def key_press_release(key: str):
    keyboard.press(key)
    time.sleep(random.uniform(0.01, 0.1))
    keyboard.release(key)


def key_press_release_no_delay(key: str):
    keyboard.press(key)
    keyboard.release(key)


上 = '8'
下 = '9'
左 = '7'
右 = '0'


def key_press_release_top():
    key_press_release(上)


def key_press_release_down():
    key_press_release(下)


def key_press_release_left():
    key_press_release(左)


def key_press_release_right():
    key_press_release(右)


def run_key(key, delay):
    key_press_release_with_delay(key, 0.1)
    key_press_release_no_delay(key)
    key_press(key)
    time.sleep(delay)
    key_release(key)


def stop_run():
    key_release(上)
    key_release(下)
    key_release(左)
    key_release(右)


def run_left(delay):
    run_key(左, delay)


def run_top(delay):
    key_press_release_with_delay(左, 0.1)
    key_press_release_no_delay(左)
    key_press(左)
    key_press(上)
    key_press(左)
    key_press(上)
    time.sleep(delay)
    key_release(上)
    key_release(左)


def run_down(delay):
    run_key(下, delay)


def run_right(delay):
    run_key(右, delay)


def calculate_current_time_difference(start_time):
    return calculate_time_difference(start_time, datetime.now(), "seconds")


# 计算时间差
def calculate_time_difference(start_time, end_time, output_type):
    time_difference = end_time - start_time

    if output_type == "seconds":
        return time_difference.total_seconds()
    elif output_type == "minutes":
        return time_difference.total_seconds() / 60
    elif output_type == "hours":
        return time_difference.total_seconds() / 3600
    else:
        return None
