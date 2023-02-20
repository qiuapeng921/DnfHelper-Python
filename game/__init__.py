from common import mem
from game import address
from game.auto import Auto
from game.func import FullScreen
from game.map_data import MapData

full_screen = FullScreen(mem)
auto = Auto(mem)
map_data = MapData(mem)


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
