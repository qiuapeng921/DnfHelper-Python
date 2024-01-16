import time

from common import helper, logger, globle, file
from game import init, mem


def check_windows(model_name) -> int:
    """
    读窗口句柄
    """
    while True:
        result = helper.find_window("地下城与勇士", "地下城与勇士：创新世纪")
        if result is not None:
            process_id = helper.get_process_id_by_name(model_name)
            if process_id != 0:
                logger.info("附加游戏成功", 1)
                return process_id
        time.sleep(0.2)


def init_config():
    """
    全局刷图计次初始化
    """
    count_cfg_name = "C:\\config.ini"
    conf_exists = file.path_exists(count_cfg_name)
    if not conf_exists:
        file.write_ini(count_cfg_name, "default", "count", "0")


def main():
    globle.cmd = "cmd"
    model_name = "DNF.exe"
    process_id = helper.get_process_id_by_name(model_name)
    if process_id == 0:
        logger.info("等待游戏运行...", 1)
        process_id = check_windows(model_name)

    mem.set_process_id(process_id)
    # 判断是否有图标
    if mem.read_int(0x140000000) != 9460301:
        raise Exception("无读写权限")
    # 初始化全局空白地址
    init.init_empty_addr()
    logger.info("加载成功-欢迎使用", 1)
    logger.info("当前时间：{}".format(helper.get_now_date()), 1)
    init.hotkey()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print("信道推出")
    except Exception as err:
        helper.print_trace("main", err)
