import sys
import traceback

from common import helper, logger, globle
from core.game import init
from core.game import mem
from plugins.driver import init_driver

if __name__ == '__main__':
    try:
        globle.cmd = "cmd"
        init_driver("win")
        logger.info("驱动加载成功", 1)
        process_id = helper.get_process_id_by_name("DNF.exe")
        if process_id == 0:
            helper.message_box("请打开dnf后运行")
            exit()

        mem.set_process_id(process_id)

        init.init_empty_addr()
        # 初始化fastcall
        init.call.init_call()
        # init.init_person()

        logger.info("加载成功-欢迎使用", 1)
        logger.info("当前时间：{}".format(helper.get_now_date()), 1)
        init.hotkey2()
    except KeyboardInterrupt as e:
        logger.file("信道推出")
    except Exception as err:
        except_type, _, except_traceback = sys.exc_info()
        err_str = ','.join(str(i) for i in err.args)
        logger.file(except_type)
        logger.file(err_str)
        for i in traceback.extract_tb(except_traceback):
            logger.file("函数{},文件:{},行:{}".format(i.name, i.filename, i.lineno))
