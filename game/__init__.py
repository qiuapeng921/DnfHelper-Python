from common import mem
from game import address, func, auto, map_data

full_screen = func.FullScreen(mem)
auto = auto.Auto(mem)
map_data = map_data.MapData(mem)


def init_empty_addr():
    """
    初始化全局空白
    """
    address.RwKbAddr = mem.allocate(2048)
    address.BuffKbAddr = mem.allocate(2048)
    address.NcBhKbAddr = mem.allocate(2048)
    address.PtGgKbAddr = mem.allocate(2048)
    address.JnKbAddr = mem.allocate(2048)
    address.GtKbAddr = mem.allocate(2048)
