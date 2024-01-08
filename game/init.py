"""
初始化全局变量
"""
import time

import keyboard

from common import globle
from game import auto as a, game_map as gm, pack as p
from game import call, traversal as tr, task as ts, screen as ac, address
from game import map_data as md
from game import mem

map_data = md.MapData(mem)
game_map = gm.GameMap()
global_data = globle.GlobalData()
pack = p.Pack()
task = ts.Task(mem, pack, map_data)
traversal = tr.Traversal(mem, pack, map_data)
screen = ac.Screen(mem, map_data)
auto = a.Auto(task, traversal, map_data, pack, game_map)


def init_empty_addr():
    """
    初始化全局空白
    """
    address.RwKbAddr = mem.allocate(2048)
    address.BuffKbAddr = mem.allocate(2048)
    address.NcBhKbAddr = mem.allocate(2048)
    address.PtGgKbAddr = mem.allocate(2048)
    address.JnKbAddr = mem.allocate(2048)
    address.GtKbAddr = mem.allocate(2048)
    address.CoolDownKbAddr = mem.allocate(2048)
    time.sleep(2)


def hotkey2():
    keyboard.add_hotkey('f1', screen.screen_switch)
    keyboard.add_hotkey('`', screen.screen_kill)
    keyboard.add_hotkey('end', auto.switch)
    keyboard.add_hotkey('ctrl+up', call.over_map_call, args=(2,))
    keyboard.add_hotkey('ctrl+down', call.over_map_call, args=(3,))
    keyboard.add_hotkey('ctrl+left', call.over_map_call, args=(0,))
    keyboard.add_hotkey('ctrl+right', call.over_map_call, args=(1,))
    # 保持程序运行
    keyboard.wait()


def hotkey():
    # 加载user32.dll
    import ctypes.wintypes
    import win32con
    import win32api
    user32 = ctypes.windll.user32
    user32.RegisterHotKey(None, 0, 0, win32con.VK_F1)
    user32.RegisterHotKey(None, 0, 0, win32con.VK_F2)
    user32.RegisterHotKey(None, 0, 0, win32con.VK_F3)
    user32.RegisterHotKey(None, 0, 0, win32con.VK_F4)
    user32.RegisterHotKey(None, 0, 0, win32con.VK_END)
    user32.RegisterHotKey(None, 0, 0, 192)  # 波浪

    user32.RegisterHotKey(None, 0, win32con.MOD_CONTROL, win32con.VK_UP)
    user32.RegisterHotKey(None, 0, win32con.MOD_CONTROL, win32con.VK_DOWN)
    user32.RegisterHotKey(None, 0, win32con.MOD_CONTROL, win32con.VK_LEFT)
    user32.RegisterHotKey(None, 0, win32con.MOD_CONTROL, win32con.VK_RIGHT)
    # user32.RegisterHotKey(None, 0, win32con.MOD_ALT, win32con.VK_UP)
    # user32.RegisterHotKey(None, 0, win32con.MOD_ALT, win32con.VK_DOWN)
    # user32.RegisterHotKey(None, 0, win32con.MOD_ALT, win32con.VK_LEFT)
    # user32.RegisterHotKey(None, 0, win32con.MOD_ALT, win32con.VK_RIGHT)

    # 以下为检测热键是否被按下，并在最后释放快捷键
    msg = ctypes.wintypes.MSG()
    while user32.GetMessageA(ctypes.byref(msg), None, 0, 0) > 0:
        if msg.message == win32con.WM_HOTKEY:
            if win32api.HIWORD(msg.lParam) == win32con.VK_F1:
                screen.screen_switch()
            if win32api.HIWORD(msg.lParam) == win32con.VK_END:
                auto.switch()
            if win32api.HIWORD(msg.lParam) == 192:
                screen.screen_kill()
            if win32api.HIWORD(msg.lParam) == win32con.VK_UP:
                call.over_map_call(2)
            if win32api.HIWORD(msg.lParam) == win32con.VK_DOWN:
                call.over_map_call(3)
            if win32api.HIWORD(msg.lParam) == win32con.VK_LEFT:
                call.over_map_call(0)
            if win32api.HIWORD(msg.lParam) == win32con.VK_RIGHT:
                call.over_map_call(1)
        else:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageA(ctypes.byref(msg))
