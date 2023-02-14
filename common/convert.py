import struct
from datetime import datetime


def GetNowDate():
    """
    get_now_date 获取系统当前日期
    :return:  string
    """
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time


def IntToBytes(int_val, int_type):
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


def FloatToBytes(float_val, float_type):
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


def AddBytes(old_bytes: bytes, *new_bytes_arr):
    """
    追加bytes
    :param old_bytes:
    :param new_bytes_arr:
    :return: bytes
    Example: add_byte(b'\x83\x84', [236, 0, 1, 0, 0], [1, 2, 3, 4]) -> b'\x83\x84\xec\x00\x01\x00\x00\x01\x02\x03\x04'
    """
    ret_bytes = AddList(list(old_bytes), *new_bytes_arr)
    return bytes(ret_bytes)


def AddList(old_list: list, *new_list_arr: list) -> list:
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


def GetEmptyBytes(count: int) -> bytes:
    result = list()
    for i in range(count):
        result.append(0)

    return bytes(result)
