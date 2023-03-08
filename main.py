import ctypes.wintypes
import os
import tempfile
import time

import win32api
import win32con

import game.map_traversal
from common import logger, globle, helper
from driver import driver
from game import mem, init, init_empty_addr

hotkey_run = True


def hotkey():
    # 加载user32.dll
    user32 = ctypes.windll.user32
    user32.RegisterHotKey(None, 0, 0, win32con.VK_F1)
    user32.RegisterHotKey(None, 0, 0, win32con.VK_F2)
    user32.RegisterHotKey(None, 0, 0, win32con.VK_F3)
    user32.RegisterHotKey(None, 0, 0, win32con.VK_F4)
    user32.RegisterHotKey(None, 0, 0, win32con.VK_END)
    user32.RegisterHotKey(None, 0, 0, 192)  # 波浪

    # user32.RegisterHotKey(None, 0, win32con.MOD_CONTROL, win32con.VK_UP)
    # user32.RegisterHotKey(None, 0, win32con.MOD_CONTROL, win32con.VK_DOWN)
    # user32.RegisterHotKey(None, 0, win32con.MOD_CONTROL, win32con.VK_LEFT)
    # user32.RegisterHotKey(None, 0, win32con.MOD_CONTROL, win32con.VK_RIGHT)
    # user32.RegisterHotKey(None, 0, win32con.MOD_ALT, win32con.VK_UP)
    # user32.RegisterHotKey(None, 0, win32con.MOD_ALT, win32con.VK_DOWN)
    # user32.RegisterHotKey(None, 0, win32con.MOD_ALT, win32con.VK_LEFT)
    # user32.RegisterHotKey(None, 0, win32con.MOD_ALT, win32con.VK_RIGHT)

    # 以下为检测热键是否被按下，并在最后释放快捷键
    msg = ctypes.wintypes.MSG()
    while hotkey_run:
        time.sleep(0.5)
        if user32.GetMessageA(ctypes.byref(msg), None, 0, 0) > 0:
            if msg.message == win32con.WM_HOTKEY:
                if win32api.HIWORD(msg.lParam) == win32con.VK_F1:
                    print("VK_F1")
                    # init.traversal.screen_switch()
                if win32api.HIWORD(msg.lParam) == win32con.VK_F2:
                    print("VK_F2")
                if win32api.HIWORD(msg.lParam) == win32con.VK_F3:
                    print("VK_F3")
                if win32api.HIWORD(msg.lParam) == win32con.VK_END:
                    init.auto.switch()
                    print("VK_END")
                if win32api.HIWORD(msg.lParam) == 192:
                    game.map_traversal.screen_kill()
                    print("波浪")
                # if win32api.HIWORD(msg.lParam) == win32con.VK_UP:
                #     print("上")
                # if win32api.HIWORD(msg.lParam) == win32con.VK_DOWN:
                #     print("下")
                # if win32api.HIWORD(msg.lParam) == win32con.VK_LEFT:
                #     print("左")
                # if win32api.HIWORD(msg.lParam) == win32con.VK_RIGHT:
                #     print("右")

            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageA(ctypes.byref(msg))


driver_name = "3swg"

if __name__ == '__main__':
    driver_path = "{}\\{}.sys".format(tempfile.gettempdir(), driver_name)

    if os.path.exists(driver_path) is False:
        logger.error("驱动不存在")
        exit()

    process_id = helper.get_process_id_by_name("DNF.exe")
    if process_id == 0:
        win32api.MessageBoxEx(0, "请打开dnf后运行", "Helper")
        exit()

    try:
        if not driver.load_driver(driver_path, driver_name, driver_name):
            logger.error("驱动加载失败")
            exit()

        logger.info("驱动加载成功")
        mem.set_process_id(process_id)
        init_empty_addr()
        import game.init
        # game.init.pack.select_map()
        data = game.init.game_map.map_data()
        print(data)
        # hotkey()
    except Exception as err:
        logger.error(err.args)
    except KeyboardInterrupt as err:
        hotkey_run = False
        logger.error(err)
    finally:
        pass
        if int(driver.hService) > 0:
            pass
        # logger.info("卸载驱动{}".format(driver.un_load_driver()))
        hotkey_run = False
