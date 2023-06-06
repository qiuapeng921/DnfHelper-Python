#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：2021-11 
@File    ：weiyang.py
@IDE     ：PyCharm 
@Author  ：Bush
@Date    ：2021/11/22 9:52
代码109006033  15471 导弹
'''
import re
import time

import file
import funciton
import judge
import tips
import tools
import traverse

import address
import call
import pack


def 玉荣判断(阶数上限, 玉荣力值):
    玉荣最低要求 = 0
    if 玉荣力值 >= 900:
        return True
    if 阶数上限 == 17:
        玉荣最低要求 = 800
    if 阶数上限 == 16:
        玉荣最低要求 = 750
    if 阶数上限 == 15:
        玉荣最低要求 = 700
    if 阶数上限 == 14:
        玉荣最低要求 = 650
    if 阶数上限 == 13:
        玉荣最低要求 = 600
    if 阶数上限 == 12:
        玉荣最低要求 = 500
    if 阶数上限 == 11:
        玉荣最低要求 = 400
    if 阶数上限 == 10:
        玉荣最低要求 = 300
    if 阶数上限 == 9:
        玉荣最低要求 = 250
    if 阶数上限 == 8:
        玉荣最低要求 = 200
    if 阶数上限 == 7:
        玉荣最低要求 = 150
    if 阶数上限 == 6:
        玉荣最低要求 = 120
    if 阶数上限 == 5:
        玉荣最低要求 = 80
    if 阶数上限 == 4:
        玉荣最低要求 = 30
    if 阶数上限 == 3:
        玉荣最低要求 = 10
    if 阶数上限 == 2:
        玉荣最低要求 = 1
    if 阶数上限 == 1:
        玉荣最低要求 = 0
    if 玉荣力值 >= 玉荣最低要求:
        return True
    else:
        return False


def decompositionOnTheCloud(position):
    """
    云上分解
    """
    pack.hccall(26)
    pack.jmcall(47, 1)
    pack.jmcall(-1, 2)
    pack.jmcall(317, 4)
    pack.jmcall(1, 1)
    pack.jmcall(position, 2)
    pack.fbcall()


def packBox(position, quantity):
    """
    组包盒子
    """
    pack.hccall(160)
    pack.jmcall(position, 2)
    pack.jmcall(quantity, 4)
    pack.fbcall()


def 门票数据(司南指针):
    global 司南阶数, 本行数据
    司南地址 = address.全局空白 + 0x512
    code = [72, 185] + tools.intTobytes(address.界面基址, 8) + [69, 49, 201] + [73, 184] + tools.intTobytes(司南指针,
                                                                                                            8) + [186]
    code = code + tools.intTobytes(address.词条ID, 4) + [255, 21, 2, 0, 0, 0, 235, 8] + tools.intTobytes(
        address.方框公告, 8)
    code = code + [72, 187] + tools.intTobytes(司南地址, 8) + [72, 137, 3]
    code = [72, 131, 236, 48] + code + [72, 131, 196, 48]
    call.asm(code)
    司南信息基址 = tools.readLongint(司南地址)
    print(f"司南信息基址 | {司南信息基址}")
    if 司南信息基址 > 0:
        司南信息首 = tools.readLongint(司南信息基址 + address.词条开始)
        司南信息尾 = tools.readLongint(司南信息基址 + address.词条结束)
        司南信息行数 = int((司南信息尾 - 司南信息首) / address.词条间隔)
        print(f"司南信息行数 | {司南信息行数}")
        for i in range(司南信息行数):
            本行指针 = tools.readLongint(司南信息首 + (i - 1) * address.词条间隔 + 32)
            if 本行指针 > 0:
                本行数据 = tools.UnicodetoAnsi(tools.read_bytes(本行指针, 100)).replace("\x00", "")
                if 本行数据 != "" and "?" not in 本行数据:
                    print(f"司南属性 | {本行数据.strip()}")
    return 本行数据.strip()


def 是否有辟邪玉():
    辟邪玉背包首 = tools.readLongint(tools.readLongint(address.辟邪玉背包) + address.物品栏偏移)
    for i in range(100):
        辟邪玉位置 = i - 1
        辟邪玉指针 = tools.readLongint(tools.readLongint(辟邪玉背包首 + (i - 1) * 32) + 16)
        if 辟邪玉指针 > 0:
            辟邪玉交易类型 = tools.readInt(辟邪玉指针 + address.交易类型, 4)
            辟邪玉品级 = tools.readInt(辟邪玉指针 + address.装备品级, 4)
            if 辟邪玉交易类型 == 1 and 辟邪玉品级 <= file.readConfiguration("洗票辟邪"):
                return True
    return False


def 计算玉荣():
    """
    自身玉荣力
    """
    return judge.superDecryption(funciton.Gets_the_pointer() + address.角色玉荣力)


class 当前玉荣:
    指针 = 0
    数值 = 0
    代码 = 0
    位置 = 0


class 临时玉荣:
    指针 = 0
    数值 = 0
    代码 = 0
    位置 = 0


class 玉荣数值:
    指针 = 0
    数值 = 0
    代码 = 0
    位置 = 0


def 玉容_call(新位置, 原位置):
    code = [65, 185] + tools.intTobytes(1, 4) + [65, 184] + tools.intTobytes(原位置, 4) + [186] + tools.intTobytes(
        新位置, 4)
    code = code + [72, 185] + tools.intTobytes(address.玉荣背包, 8) + [72, 139, 9, 72, 184] + tools.intTobytes(
        address.物品移动CALL, 8) + [255, 208]
    code = [72, 131, 236, 48] + code + [72, 131, 196, 48, 195]
    call.asm(code)


def 最大玉荣(玉荣颜色):
    global 当前玉荣
    背包地址 = tools.readLongint(tools.readLongint(address.玉荣背包) + address.物品栏偏移) + address.玉荣栏偏移
    for i in range(100):
        局_玉荣指针 = tools.readLongint(tools.readLongint(背包地址 + (i - 1) * 32) + 16)
        if 局_玉荣指针 != 0:
            交易类型 = tools.readInt(局_玉荣指针 + address.交易类型, 4)
            # print(f"交易类型 | {交易类型}")
            if 交易类型 != 0:
                临时玉荣.数值 = tools.readInt(局_玉荣指针 + address.玉荣力偏移, 4)
                临时玉荣.代码 = tools.readInt(局_玉荣指针 + address.装备代码, 4)
                临时玉荣.指针 = 局_玉荣指针
                临时玉荣.位置 = i
                # print(临时玉荣.代码)
                if 临时玉荣.数值 > 当前玉荣.数值 and 临时玉荣.数值 < 300:
                    if 玉荣颜色 == 1:
                        if 临时玉荣.代码 == 400410175 or 临时玉荣.代码 == 400410000:
                            当前玉荣 = 临时玉荣
                    if 玉荣颜色 == 2:  # 绿色
                        if 临时玉荣.代码 == 400410182 or 临时玉荣.代码 == 400410001:
                            当前玉荣 = 临时玉荣
                    if 玉荣颜色 == 3:  # 蓝色
                        if 临时玉荣.代码 == 400410183 or 临时玉荣.代码 == 400410002:
                            当前玉荣 = 临时玉荣
            return 当前玉荣


def 玉荣穿戴():
    global 玉荣数值
    局_一级地址 = tools.readLongint(tools.readLongint(address.辟邪玉背包) + address.物品栏偏移)
    原值 = 计算玉荣()
    print(f"原值玉荣 | {原值}")
    for i in range(202, 210):
        局_玉荣指针 = tools.readLongint(tools.readLongint(局_一级地址 + (i - 1) * 32) + 16)
        临时数值 = tools.readInt(局_玉荣指针 + address.玉荣力偏移, 4)
        if i == 204 or i == 202 or i == 203:  # 红色位置
            玉荣数值 = 最大玉荣(1)
            if 玉荣数值.数值 > 临时数值 and 临时数值 < 1300:
                玉容_call(i - 1, 玉荣数值.位置 + 99)
                time.sleep(0.5)
        if i == 209 or i == 208:  # 绿色位置
            玉荣数值 = 最大玉荣(2)
            if 玉荣数值.数值 > 临时数值 and 临时数值 < 1300:
                玉容_call(i - 1, 玉荣数值.位置 + 99)
                time.sleep(0.5)
        if i == 205 or i == 206 or i == 207:  # 蓝色位置
            玉荣数值 = 最大玉荣(3)
            if 玉荣数值.数值 > 临时数值 and 临时数值 < 1300:
                玉容_call(i - 1, 玉荣数值.位置 + 99)
                time.sleep(0.5)

    新值 = 计算玉荣()
    if 新值 > 原值:
        print(f"增加玉荣力 {新值 - 原值}")


def sinanAddsCall(sinanLocation):
    """
    司南添加CALL
    """
    data = [72, 129, 236, 0, 1, 0, 0, 72, 186] + tools.intTobytes(sinanLocation, 8) + [72, 185] + tools.intTobytes(
        address.取司南添加RCX, 8)
    data = data + [255, 21, 2, 0, 0, 0, 235, 8] + tools.intTobytes(address.司南添加CALL, 8)
    data = data + [72, 129, 196, 0, 1, 0, 0]
    call.asm(data)


def siNanJintuCALL(sinanBackpackLocation):
    """
    司南进图CALL
    """
    data = [0x48, 0x83, 0xEC, 0x30, 0xBA] + tools.intTobytes(sinanBackpackLocation, 4) + [0x48,
                                                                                          0xB9] + tools.intTobytes(
        address.司南进图_Rcx, 8)
    data = data + [0x48, 0x8B, 0x09, 0x48, 0xB8] + tools.intTobytes(address.司南进图CALL, 8)
    data = data + [0xFF, 0xD0, 0x48, 0x83, 0xC4, 0x30]
    call.asm(data)


def takeSinanAndAddRcx():
    """
    取司南添加Rcx
    """
    data = [0x48, 0x83, 0xEC, 0x30, 0x45, 0x31, 0xC0, 0xBA] + tools.intTobytes(412, 8) + [0x48, 0xB9]
    data = data + tools.intTobytes(address.商店基址, 8) + [0x48, 0x8B, 0x09, 0x48, 0xB8]
    data = data + tools.intTobytes(address.取司南添加RCX, 8) + [0xFF, 0xD0]
    data = data + [0x48, 0x83, 0xC4, 0x30]
    call.asm(data)


def whetherOnTheCloud(name):
    """
    是否云上
    """
    if '重' in name or '试炼' in name:
        return True
    else:
        return False


def trialTicket(sinanName):
    """
    是否试炼票
    """
    if '试炼' in sinanName:
        return True
    else:
        return False


def ticketsForYurongli(sinanName):
    """
    门票玉荣力
    """
    if '1阶' in sinanName:
        return 0
    if '2阶' in sinanName:
        return 1
    if '3阶' in sinanName:
        return 10
    if '4阶' in sinanName:
        return 30
    if '5阶' in sinanName:
        return 80
    if '6阶' in sinanName:
        return 120
    if '7阶' in sinanName:
        return 150
    if '8阶' in sinanName:
        return 200
    if '9阶' in sinanName:
        return 250
    if '10阶' in sinanName:
        return 300
    if '11阶' in sinanName:
        return 400
    if '12阶' in sinanName:
        return 500
    if '13阶' in sinanName:
        return 600
    if '14阶' in sinanName:
        return 700
    if '15阶' in sinanName:
        return 800
    if '16阶' in sinanName:
        return 900
    if '17阶' in sinanName:
        return 1000
    if '18阶' in sinanName:
        return 1100
    else:
        return -1


def 残月宫阙1至5阶():
    当前坐标 = traverse.getCurrentRoom()
    顺图变量 = 0
    if 当前坐标[0] == 0 and 当前坐标[1] == 1:
        顺图变量 = 0
        return 1
    if 当前坐标[0] == 1 and 当前坐标[1] == 1 and 顺图变量 == 0:
        return 3
    if 当前坐标[0] == 1 and 当前坐标[1] == 2:
        顺图变量 = 1
        return 2
    if 当前坐标[0] == 2 and 当前坐标[1] == 1 and 顺图变量 == 1:
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 1:
        顺图变量 = 2
        return 0
    if 当前坐标[0] == 1 and 当前坐标[1] == 1 and 顺图变量 == 2:
        return 2
    if 当前坐标[0] == 1 and 当前坐标[1] == 0:
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 0:
        return 1
    if 当前坐标[0] == 3 and 当前坐标[1] == 0:
        return 3
    else:
        return -1


def 沧池竹林1至5阶():
    当前坐标 = traverse.getCurrentRoom()
    顺图变量 = 0
    if 当前坐标[0] == 0 and 当前坐标[1] == 1:
        顺图变量 = 0
        return 1
    if 当前坐标[0] == 1 and 当前坐标[1] == 1:
        return 2
    if 当前坐标[0] == 1 and 当前坐标[1] == 0:
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 0:
        return 3
    if 当前坐标[0] == 2 and 当前坐标[1] == 1 and 顺图变量 == 0:
        return 3
    if 当前坐标[0] == 2 and 当前坐标[1] == 2:
        顺图变量 = 1
        return 2
    if 当前坐标[0] == 2 and 当前坐标[1] == 1 and 顺图变量 == 1:
        return 1
    else:
        return -1


def 幻境前殿1至5阶():
    当前坐标 = traverse.getCurrentRoom()
    顺图变量 = 0
    if 当前坐标[0] == 0 and 当前坐标[1] == 1:
        顺图变量 = 0
        return 1
    if 当前坐标[0] == 1 and 当前坐标[1] == 1 and 顺图变量 == 0:
        return 3
    if 当前坐标[0] == 1 and 当前坐标[1] == 2:
        顺图变量 = 1
        return 2
    if 当前坐标[0] == 1 and 当前坐标[1] == 1 and 顺图变量 == 1:
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 1 and 顺图变量 == 1:
        return 2
    if 当前坐标[0] == 2 and 当前坐标[1] == 0:
        顺图变量 = 2
        return 3
    if 当前坐标[0] == 2 and 当前坐标[1] == 1 and 顺图变量 == 2:
        return 1
    else:
        return -1


def 未央之脊1至5阶():
    当前坐标 = traverse.getCurrentRoom()
    顺图变量 = 0
    if 当前坐标[0] == 0 and 当前坐标[1] == 1:
        return 1
    if 当前坐标[0] == 1 and 当前坐标[1] == 1:
        顺图变量 == 0
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 1:
        return 1
    if 当前坐标[0] == 3 and 当前坐标[1] == 1 and 顺图变量 == 0:
        return 2
    if 当前坐标[0] == 3 and 当前坐标[1] == 0:
        顺图变量 = 1
        return 3
    if 当前坐标[0] == 3 and 当前坐标[1] == 1 and 顺图变量 == 1:
        return 1
    else:
        return -1


def 沧池竹林6至10阶():
    当前坐标 = traverse.getCurrentRoom()
    顺图变量 = 0
    if 当前坐标[0] == 0 and 当前坐标[1] == 1:
        return 1
    if 当前坐标[0] == 1 and 当前坐标[1] == 1:
        return 2
    if 当前坐标[0] == 1 and 当前坐标[1] == 0:
        顺图变量 = 0
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 0:
        return 1
    if 当前坐标[0] == 3 and 当前坐标[1] == 0:
        return 3
    if 当前坐标[0] == 3 and 当前坐标[1] == 1 and 顺图变量 == 0:
        return 3
    if 当前坐标[0] == 3 and 当前坐标[1] == 2:
        顺图变量 = 1
        return 2
    if 当前坐标[0] == 3 and 当前坐标[1] == 1 and 顺图变量 == 1:
        return 0
    if 当前坐标[0] == 2 and 当前坐标[1] == 1:
        顺图变量 = 2
        return 1
    if 当前坐标[0] == 3 and 当前坐标[1] == 1 and 顺图变量 == 2:
        return 1
    else:
        return -1


def 残月宫阙6至10阶():
    当前坐标 = traverse.getCurrentRoom()
    顺图变量 = 0
    if 当前坐标[0] == 0 and 当前坐标[1] == 1:
        顺图变量 = 0
        return 1
    if 当前坐标[0] == 1 and 当前坐标[1] == 1:
        return 2
    if 当前坐标[0] == 1 and 当前坐标[1] == 1 and 顺图变量 == 0:
        return 3
    if 当前坐标[0] == 1 and 当前坐标[1] == 2:
        顺图变量 = 1
        return 2
    if 当前坐标[0] == 1 and 当前坐标[1] == 1 and 顺图变量 == 1:
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 1 and 顺图变量 == 1:
        return 3
    if 当前坐标[0] == 2 and 当前坐标[1] == 2:
        顺图变量 = 2
        return 2
    if 当前坐标[0] == 2 and 当前坐标[1] == 1 and 顺图变量 == 2:
        return 0
    if 当前坐标[0] == 1 and 当前坐标[1] == 1 and 顺图变量 == 2:
        return 2
    if 当前坐标[0] == 1 and 当前坐标[1] == 0:
        顺图变量 = 3
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 0:
        return 1
    if 当前坐标[0] == 3 and 当前坐标[1] == 0 and 顺图变量 == 3:
        return 1
    if 当前坐标[0] == 4 and 当前坐标[1] == 0:
        顺图变量 = 4
        return 0
    if 当前坐标[0] == 3 and 当前坐标[1] == 0 and 顺图变量 == 4:
        return 3
    else:
        return -1


def 幻境前殿6至10阶():
    当前坐标 = traverse.getCurrentRoom()
    顺图变量 = 0
    if 当前坐标[0] == 0 and 当前坐标[1] == 1:
        顺图变量 = 0
        return 1
    if 当前坐标[0] == 1 and 当前坐标[1] == 1 and 顺图变量 == 0:
        return 3
    if 当前坐标[0] == 1 and 当前坐标[1] == 2 and 顺图变量 == 0:
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 2:
        顺图变量 = 1
        return 0
    if 当前坐标[0] == 1 and 当前坐标[1] == 2 and 顺图变量 == 1:
        return 2
    if 当前坐标[0] == 1 and 当前坐标[1] == 1 and 顺图变量 == 1:
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 1 and 顺图变量 == 1:
        return 2
    if 当前坐标[0] == 2 and 当前坐标[1] == 0 and 顺图变量 == 1:
        return 0
    if 当前坐标[0] == 1 and 当前坐标[1] == 0:
        顺图变量 = 2
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 0 and 顺图变量 == 2:
        return 3
    if 当前坐标[0] == 2 and 当前坐标[1] == 1 and 顺图变量 == 2:
        return 1
    else:
        return -1


def 未央之脊6至10阶():
    当前坐标 = traverse.getCurrentRoom()
    顺图变量 = 0
    if 当前坐标[0] == 0 and 当前坐标[1] == 1:
        顺图变量 = 0
        return 1
    if 当前坐标[0] == 1 and 当前坐标[1] == 1:
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 1 and 顺图变量 == 0:
        return 3
    if 当前坐标[0] == 2 and 当前坐标[1] == 2:
        顺图变量 = 1
        return 2
    if 当前坐标[0] == 2 and 当前坐标[1] == 1 and 顺图变量 == 1:
        return 1
    if 当前坐标[0] == 3 and 当前坐标[1] == 1:
        return 1
    if 当前坐标[0] == 4 and 当前坐标[1] == 1 and 顺图变量 == 1:
        return 2
    if 当前坐标[0] == 4 and 当前坐标[1] == 0:
        顺图变量 = 2
        return 3
    if 当前坐标[0] == 4 and 当前坐标[1] == 1 and 顺图变量 == 2:
        return 1
    else:
        return -1


def 幻境前殿11至15阶():
    当前坐标 = traverse.getCurrentRoom()
    顺图变量 = 0
    if 当前坐标[0] == 0 and 当前坐标[1] == 1:
        顺图变量 = 0
        return 1
    if 当前坐标[0] == 1 and 当前坐标[1] == 1 and 顺图变量 == 0:
        return 3
    if 当前坐标[0] == 1 and 当前坐标[1] == 2 and 顺图变量 == 0:
        return 0
    if 当前坐标[0] == 0 and 当前坐标[1] == 2:
        顺图变量 = 1
        return 1
    if 当前坐标[0] == 1 and 当前坐标[1] == 2 and 顺图变量 == 1:
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 2:
        顺图变量 = 2
        return 0
    if 当前坐标[0] == 1 and 当前坐标[1] == 2 and 顺图变量 == 2:
        return 2
    if 当前坐标[0] == 1 and 当前坐标[1] == 1 and 顺图变量 == 2:
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 1 and 顺图变量 == 2:
        return 2
    if 当前坐标[0] == 2 and 当前坐标[1] == 0 and 顺图变量 == 2:
        return 0
    if 当前坐标[0] == 1 and 当前坐标[1] == 0:
        顺图变量 = 3
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 0 and 顺图变量 == 3:
        return 3
    if 当前坐标[0] == 2 and 当前坐标[1] == 1 and 顺图变量 == 3:
        return 1
    else:
        return -1


def 沧池竹林11至15阶():
    当前坐标 = traverse.getCurrentRoom()
    顺图变量 = 0
    if 当前坐标[0] == 0 and 当前坐标[1] == 1:
        顺图变量 = 0
        return 1
    if 当前坐标[0] == 1 and 当前坐标[1] == 1:
        return 2
    if 当前坐标[0] == 1 and 当前坐标[1] == 0 and 顺图变量 == 0:
        return 0
    if 当前坐标[0] == 0 and 当前坐标[1] == 0:
        顺图变量 = 1
        return 1
    if 当前坐标[0] == 1 and 当前坐标[1] == 0 and 顺图变量 == 1:
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 0:
        return 1
    if 当前坐标[0] == 3 and 当前坐标[1] == 0:
        return 3
    if 当前坐标[0] == 3 and 当前坐标[1] == 1 and 顺图变量 == 1:
        return 3
    if 当前坐标[0] == 3 and 当前坐标[1] == 2:
        顺图变量 = 2
        return 2
    if 当前坐标[0] == 3 and 当前坐标[1] == 1 and 顺图变量 == 2:
        return 0
    if 当前坐标[0] == 2 and 当前坐标[1] == 1:
        顺图变量 = 3
        return 1
    if 当前坐标[0] == 3 and 当前坐标[1] == 1 and 顺图变量 == 3:
        return 1
    else:
        return -1


def 残月宫阙11至15阶():
    当前坐标 = traverse.getCurrentRoom()
    顺图变量 = 0
    if 当前坐标[0] == 0 and 当前坐标[1] == 1:
        顺图变量 = 0
        return 1
    if 当前坐标[0] == 1 and 当前坐标[1] == 1 and 顺图变量 == 0:
        return 3
    if 当前坐标[0] == 1 and 当前坐标[1] == 2:
        顺图变量 = 1
        return 2
    if 当前坐标[0] == 1 and 当前坐标[1] == 1 and 顺图变量 == 1:
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 1 and 顺图变量 == 1:
        return 3
    if 当前坐标[0] == 2 and 当前坐标[1] == 2:
        顺图变量 = 2
        return 2
    if 当前坐标[0] == 2 and 当前坐标[1] == 1 and 顺图变量 == 2:
        return 0
    if 当前坐标[0] == 1 and 当前坐标[1] == 1 and 顺图变量 == 2:
        return 2
    if 当前坐标[0] == 1 and 当前坐标[1] == 0 and 顺图变量 == 2:
        return 0
    if 当前坐标[0] == 0 and 当前坐标[1] == 0:
        顺图变量 = 3
        return 1
    if 当前坐标[0] == 1 and 当前坐标[1] == 0 and 顺图变量 == 3:
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 0 and 顺图变量 == 3:
        return 1
    if 当前坐标[0] == 3 and 当前坐标[1] == 0 and 顺图变量 == 3:
        return 1
    if 当前坐标[0] == 4 and 当前坐标[1] == 0:
        顺图变量 = 4
        return 0
    if 当前坐标[0] == 3 and 当前坐标[1] == 0 and 顺图变量 == 4:
        return 3
    else:
        return -1


def 未央之脊11至15阶():
    当前坐标 = traverse.getCurrentRoom()
    顺图变量 = 0
    if 当前坐标[0] == 0 and 当前坐标[1] == 1:
        顺图变量 = 0
        return 1
    if 当前坐标[0] == 1 and 当前坐标[1] == 1 and 顺图变量 == 0:
        return 2
    if 当前坐标[0] == 1 and 当前坐标[1] == 0:
        顺图变量 = 1
        return 3
    if 当前坐标[0] == 1 and 当前坐标[1] == 1 and 顺图变量 == 1:
        return 1
    if 当前坐标[0] == 2 and 当前坐标[1] == 1 and 顺图变量 == 1:
        return 3
    if 当前坐标[0] == 2 and 当前坐标[1] == 2:
        顺图变量 = 2
        return 2
    if 当前坐标[0] == 2 and 当前坐标[1] == 1 and 顺图变量 == 2:
        return 1
    if 当前坐标[0] == 3 and 当前坐标[1] == 1:
        return 1
    if 当前坐标[0] == 4 and 当前坐标[1] == 1 and 顺图变量 == 2:
        return 2
    if 当前坐标[0] == 4 and 当前坐标[1] == 0:
        顺图变量 = 3
        return 3
    if 当前坐标[0] == 4 and 当前坐标[1] == 1 and 顺图变量 == 3:
        return 1
    else:
        return -1


def evilJade():
    """
    辟邪玉分解
    """
    global index
    backpackStart = tools.readLongint(tools.readLongint(address.玉荣背包) + address.背包指针)
    for index in range(100):
        backpackAddress = tools.readLongint(tools.readLongint(backpackStart + (index - 1) * 32) + 16)
        if backpackAddress != 0:
            transactionType = tools.readInt(backpackAddress + address.交易类型, 4)
            equipmentGrade = tools.readInt(backpackAddress + address.装备品级, 4)
            if equipmentGrade == 0 or equipmentGrade == 1 or equipmentGrade == 2:
                if transactionType != 0 or transactionType != 3:
                    decompositionOnTheCloud(index - 1)
                    index += 1
    tips.notice('辟邪玉分解< ' + str(index) + ' >', 1)


def decomposeYurong():
    """
    分解玉荣
    """
    global index
    backpackStart = tools.readLongint(tools.readLongint(address.玉荣背包) + address.背包指针) + address.玉荣栏偏移
    for index in range(100):
        backpackAddress = tools.readLongint(tools.readLongint(backpackStart + (index - 1) * 32) + 16)
        if backpackAddress != 0:
            transactionType = tools.readInt(backpackAddress + address.交易类型, 4)
            equipmentGrade = tools.readInt(backpackAddress + address.装备品级, 4)
            numberOfYurong = tools.readInt(backpackAddress + address.玉荣力偏移, 4)
            if numberOfYurong > 0:
                if equipmentGrade == 0 or equipmentGrade == 1 or equipmentGrade == 2:
                    decompositionOnTheCloud(index + 100 - 1)
                    index += 1
    tips.notice('玉荣分解< ' + str(index) + ' >', 1)


def 顺序放票(玉荣力值):
    玉荣名称 = ""
    单人不可交易 = file.readConfiguration("单人不可交易最高刷到")
    单可交易司南 = file.readConfiguration("单人交易司南最高刷到")
    单人试炼司南 = file.readConfiguration("单人试炼司南最高刷到")
    组队不可交易 = file.readConfiguration("组队不可交易最高刷到")
    组可交易司南 = file.readConfiguration("组队交易司南最高刷到")
    组队试炼司南 = file.readConfiguration("组队试炼司南最高刷到")
    背包首 = tools.readLongint(tools.readLongint(address.司南背包) + address.背包指针)
    for i in range(100):
        物品地址 = tools.readLongint(tools.readLongint(背包首 + (index - 1) * 32) + 16)
        if 物品地址 != 0:
            物品名称 = tools.UnicodetoAnsi(
                tools.read_bytes(tools.readLongint(物品地址 + address.物品名称), 50)).replace("\x00", "")
            交易类型 = tools.readInt(物品地址 + address.交易类型, 4)
            司南类型 = tools.readInt(tools.readLongint(物品名称 + address.司南类型_1) + address.司南类型_2, 4)
            司南阶数 = int(re.findall("\d+", 物品名称)[0])
            票数据 = 门票数据(物品地址)
            if "试炼" in 物品名称:
                if "单人" in 票数据:
                    if 司南阶数 < 单人试炼司南:
                        if 玉荣判断(司南阶数, 玉荣力值) == True:
                            return i - 1
                    if 司南阶数 < 组队试炼司南:
                        if 玉荣判断(司南阶数, 玉荣力值) == True:
                            return i - 1
                if 交易类型 > 0:
                    if "单人" in 票数据:
                        if 司南阶数 < 单可交易司南:
                            if 玉荣判断(司南阶数, 玉荣力值) == True:
                                return i - 1
                        if 司南阶数 < 组可交易司南:
                            if 玉荣判断(司南阶数, 玉荣力值) == True:
                                return i - 1
                        if 司南阶数 < 单人不可交易:
                            if 玉荣判断(司南阶数, 玉荣力值) == True:
                                return i - 1
                        if 司南阶数 < 组队不可交易:
                            if 玉荣判断(司南阶数, 玉荣力值) == True:
                                return i - 1


def 未央选图():
    if tools.readInt(address.城镇大区域, 4) != 126:
        print("请在未央频道开启本自动模式")
        return
    if tools.readInt(address.城镇小区域, 4) != 2:
        call.townMobileCall(126, 2, 26, 335)
    if file.readConfiguration("穿戴玉荣") == 1:
        玉荣穿戴()
    if file.readConfiguration("玉荣分解") == 1:
        decomposeYurong()
    if file.readConfiguration("辟邪分解") == 1:
        evilJade()
    if file.readConfiguration("开幻境箱") == 1 and traverse.pickUpTheNumberOfItems("幻境宝箱", 0) > 0:
        while traverse.pickUpTheNumberOfItems("幻境宝箱", 0) > 0:
            pack.pack_out_of_the_box(traverse.pickUpTheNumberOfItems("幻境宝箱", 1))
            time.sleep(0.5)
