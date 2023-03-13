import struct
from datetime import datetime

import psutil
import random

import win32api


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


hr_t, min_t, sec_t = (0, 0, 0)


def get_app_run_time():
    """获取app运行时间"""
    global hr_t, min_t, sec_t
    sec_t = sec_t + 1
    if sec_t == 60:
        sec_t = 0
        min_t = min_t + 1
    if min_t == 60:
        min_t = 0
        hr_t = hr_t + 1
    string = "{}:{}:{}".format(hr_t, min_t, sec_t)
    return string


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
        return struct.pack('<h', int_val)
    if int_type == 4:
        return struct.pack('<i', int_val)
    if int_type == 8:
        return struct.pack('<q', int_val)


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
