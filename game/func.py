import _thread
import time

from common import convert


class FullScreen:
    __switch = False

    mem = None

    def __init__(self, mem):
        self.mem = mem
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
            print(convert.get_now_date())
            time.sleep(1)

    def stop(self):
        self.__switch = False
