from common import memory
from game import address


def init_empty_addr():
    """
    初始化全局空白
    :return:
    """
    pm = memory.Memory()
    address.RwKbAddr = pm.memory().allocate(2048)
    address.BuffKbAddr = pm.memory().allocate(2048)
    address.NcBhKbAddr = pm.memory().allocate(2048)
    address.PtGgKbAddr = pm.memory().allocate(2048)
    address.JnKbAddr = pm.memory().allocate(2048)
    address.GtKbAddr = pm.memory().allocate(2048)
