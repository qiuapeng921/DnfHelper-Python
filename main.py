import tempfile

from common import helper
from driver import driver
from game import mem, init

driver_name = "3swg"

if __name__ == '__main__':
    driver_path = "{}\\{}.sys".format(tempfile.gettempdir(), driver_name)
    import os

    if os.path.exists(driver_path) is False:
        print("驱动不存在")
        exit()

    process_id = helper.get_process_id_by_name("DNF.exe")
    if process_id == 0:
        helper.message_box("请打开dnf后运行")
        exit()

    try:
        if not driver.load_driver(driver_path, driver_name, driver_name):
            print("驱动加载失败")
            exit()

        print("驱动加载成功")
        mem.set_process_id(process_id)
        init.init_empty_addr()
        data = init.game_map.map_data()
        print(data)
        # hotkey()
        i = 0
    except Exception as err:
        import sys
        import traceback

        except_type, _, except_traceback = sys.exc_info()
        print(except_type)
        print(err.args)
        print(except_traceback)
        print('-----------')
        for i in traceback.extract_tb(except_traceback):
            print(i)
    except KeyboardInterrupt as err:
        print(err)
    finally:
        pass
