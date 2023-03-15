"""
初始化全局变量
"""
import keyboard

from common import globle
from game import auto as a, address, other as o, task as t, call
from game import map_data as md, game_map as gm, map_traversal as mt, pack as p
from game import mem

traversal = mt.Screen(mem)
map_data = md.MapData(mem)
game_map = gm.GameMap()
global_data = globle.GlobalData()
pack = p.Pack()
task = t.Task(mem, pack, map_data)
pick = o.Pickup(mem, pack, map_data)
equip = o.Equip(mem, pack, map_data)
auto = a.Auto(task, traversal, global_data, map_data, pack, pick,equip,game_map)


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


hotkey_run = True


def hotkey2():
    keyboard.add_hotkey('f1', traversal.screen_switch)
    keyboard.add_hotkey('`', traversal.screen_kill)
    keyboard.add_hotkey('end', auto.switch)
    # 保持程序运行
    keyboard.wait()


def hotkey():
    # 加载user32.dll
    import ctypes.wintypes
    import win32con
    import win32api
    import time
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
    while hotkey_run:
        time.sleep(0.1)
        if user32.GetMessageA(ctypes.byref(msg), None, 0, 0) > 0:
            if msg.message == win32con.WM_HOTKEY:
                if win32api.HIWORD(msg.lParam) == win32con.VK_F1:
                    traversal.screen_switch()
                if win32api.HIWORD(msg.lParam) == win32con.VK_END:
                    auto.switch()
                if win32api.HIWORD(msg.lParam) == 192:
                    traversal.screen_kill()
                if win32api.HIWORD(msg.lParam) == win32con.VK_UP:
                    call.over_map_call(2)
                if win32api.HIWORD(msg.lParam) == win32con.VK_DOWN:
                    call.over_map_call(3)
                if win32api.HIWORD(msg.lParam) == win32con.VK_LEFT:
                    call.over_map_call(0)
                if win32api.HIWORD(msg.lParam) == win32con.VK_RIGHT:
                    call.over_map_call(1)
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageA(ctypes.byref(msg))
