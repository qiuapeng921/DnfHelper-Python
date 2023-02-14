import time

from common import convert
import _thread


class FullScreen:
    __switch = False

    def __init__(self):
        pass

    def switch(self):
        """
        技能全屏
        """
        self.__switch = not self.__switch
        if self.__switch:
            _thread.start_new_thread(self.run, ())
            print("技能全屏开启")
        else:
            self.__switch = False
            print("技能全屏关闭")

    def run(self):
        while self.__switch:
            print(convert.GetNowDate())
            time.sleep(1)

    def stop(self):
        self.__switch = False
