from core.driver.derive import MemoryRw

driver = MemoryRw()


def init_driver(driver_name: str):
    driver_path = "C:\\{}.sys".format(driver_name)
    import os
    if os.path.exists(driver_path) is False:
        raise Exception("驱动不存在")

    if not driver.load_driver(driver_path, driver_name, driver_name):
        raise Exception("驱动加载失败")
