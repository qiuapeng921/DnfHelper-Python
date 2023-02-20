import ctypes
import ctypes.wintypes
import time

import win32api
import win32con


class Hotkey:
    def __init__(self):
        super().__init__()
        self.running = True

    def stop(self):
        self.running = False
        user32 = ctypes.windll.user32
        for e in [win32con.VK_F1, win32con.VK_F2, win32con.VK_F3, win32con.VK_F4]:
            user32.UnregisterHotKey(None, e)

    def run(self):
        # 加载user32.dll
        user32 = ctypes.windll.user32
        user32.RegisterHotKey(None, 0, 0, win32con.VK_F1)
        user32.RegisterHotKey(None, 0, 0, win32con.VK_F2)
        user32.RegisterHotKey(None, 0, 0, win32con.VK_F3)
        user32.RegisterHotKey(None, 0, 0, win32con.VK_F4)
        user32.RegisterHotKey(None, 0, 0, 192)  # 波浪
        user32.RegisterHotKey(None, 0, win32con.MOD_CONTROL, win32con.VK_UP)
        user32.RegisterHotKey(None, 0, win32con.MOD_CONTROL, win32con.VK_DOWN)
        user32.RegisterHotKey(None, 0, win32con.MOD_CONTROL, win32con.VK_LEFT)
        user32.RegisterHotKey(None, 0, win32con.MOD_CONTROL, win32con.VK_RIGHT)
        user32.RegisterHotKey(None, 0, win32con.MOD_ALT, win32con.VK_UP)
        user32.RegisterHotKey(None, 0, win32con.MOD_ALT, win32con.VK_DOWN)
        user32.RegisterHotKey(None, 0, win32con.MOD_ALT, win32con.VK_LEFT)
        user32.RegisterHotKey(None, 0, win32con.MOD_ALT, win32con.VK_RIGHT)

        # 以下为检测热键是否被按下，并在最后释放快捷键
        msg = ctypes.wintypes.MSG()
        while self.running:
            if user32.GetMessageA(ctypes.byref(msg), None, 0, 0) > 0:
                if msg.message == win32con.WM_HOTKEY:
                    if win32api.HIWORD(msg.lParam) == win32con.VK_F1:
                        print("VK_F1")
                    if win32api.HIWORD(msg.lParam) == win32con.VK_F2:
                        print("VK_F2")
                    if win32api.HIWORD(msg.lParam) == win32con.VK_F3:
                        print("VK_F3")
                    if win32api.HIWORD(msg.lParam) == 192:
                        print("波浪")
                    if win32api.HIWORD(msg.lParam) == win32con.VK_UP:
                        print("上")
                    if win32api.HIWORD(msg.lParam) == win32con.VK_DOWN:
                        print("下")
                    if win32api.HIWORD(msg.lParam) == win32con.VK_LEFT:
                        print("左")
                    if win32api.HIWORD(msg.lParam) == win32con.VK_RIGHT:
                        print("右")
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageA(ctypes.byref(msg))
            time.sleep(0.1)
