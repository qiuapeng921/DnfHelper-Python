import sys

import win32api

from api.hotkey import Hotkey
from common import helper, logger, globle, mem
from driver import driver
from game import init_empty_addr

hotkey = Hotkey()

if __name__ == '__main__':
    process_id = helper.get_process_id_by_name("DNF.exe")

    if process_id == 0:
        win32api.MessageBoxEx(0, "请打开dnf后运行", "Helper")
        sys.exit(1)

    try:
        path = "C:\\RanRw.sys"
        if not driver.load_driver(path, "RanRw", "RanRw"):
            logger.error("驱动加载失败")
            sys.exit()

        logger.info("驱动加载成功")
        globle.process_id = process_id
        mem.set_process_id(globle.process_id)
        init_empty_addr()
        hotkey.run()

    except Exception as err:
        logger.error(err.args)
        logger.info("卸载驱动{}".format(driver.un_load_driver()))
    except KeyboardInterrupt as err:
        hotkey.stop()
        switch = False
        logger.error(err)
        pass
    finally:
        hotkey.stop()
        pass
