from common import helper, globle, logger
from driver import init_driver
from game import mem, init

if __name__ == '__main__':
    try:
        globle.cmd = "cmd"
        init_driver()
        logger.info("驱动加载成功")
        process_id = helper.get_process_id_by_name("DNF.exe")
        if process_id == 0:
            helper.message_box("请打开dnf后运行")
            exit()

        mem.set_process_id(process_id)
        init.init_empty_addr()
        init.hotkey()
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
