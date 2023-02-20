import ctypes
import ctypes.wintypes

import win32con


class Hotkey:
    def __init__(self):
        super().__init__()
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        # 加载user32.dll
        user32 = ctypes.windll.user32
        user32.RegisterHotKey(None, win32con.VK_F1, 0, win32con.VK_F1)
        user32.RegisterHotKey(None, win32con.VK_F2, 0, win32con.VK_F2)
        user32.RegisterHotKey(None, win32con.VK_F3, 0, win32con.VK_F3)
        user32.RegisterHotKey(None, win32con.VK_F4, 0, win32con.VK_F4)
        user32.RegisterHotKey(None, win32con.VK_END, 0, win32con.VK_END)
        user32.RegisterHotKey(None, win32con.MOD_ALT, win32con.MOD_ALT, win32con.VK_UP)

        # 以下为检测热键是否被按下，并在最后释放快捷键
        try:
            msg = ctypes.wintypes.MSG()
            while self.running:
                if user32.GetMessageA(ctypes.byref(msg), None, 0, 0) > 0:
                    print(msg.message)
                    print(msg.wParam)
                    if msg.message == win32con.WM_HOTKEY:
                        if msg.wParam == win32con.VK_F1:
                            print("VK_F1")
                            pass
                        if msg.wParam == win32con.VK_END:
                            print("logout")
                            self.running = False

                    # 按下ALT
                    if msg.message == win32con.WM_SYSKEYDOWN:
                        if msg.wParam == win32con.VK_UP:
                            print("VK_UP")
                            pass

                    user32.TranslateMessage(ctypes.byref(msg))
                    user32.DispatchMessageA(ctypes.byref(msg))

        finally:
            for e in [win32con.VK_F1, win32con.VK_F2, win32con.VK_F3, win32con.VK_F4]:
                user32.UnregisterHotKey(None, e)
