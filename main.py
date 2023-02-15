import sys

import keyboard

from common import globle, mem
from common.logger import logger
from driver import driver
from game.func import FullScreen

if __name__ == '__main__':
    try:
        path = "C:\\RanRw.sys"
        if not driver.load_driver(path, "RanRw", "RanRw"):
            logger.error("驱动加载失败")
            sys.exit()

        logger.info("驱动加载成功")
        globle.process_id = 5080
        mem.set_process_id(globle.process_id)

        full_screen = FullScreen()
        keyboard.add_hotkey('END', full_screen.switch)
        keyboard.wait()

        while 1:
            keyboard.wait('')
    except Exception as err:
        print(err.args)
    except KeyboardInterrupt as err:
        print(err)
        pass
    finally:
        print("卸载驱动{}".format(driver.un_load_driver()))
