"""
初始化全局变量
"""

from common import mem
from game.auto import Auto
from game.func import FullScreen
from game.map_data import MapData
from game.structure import GlobalData

full_screen = FullScreen(mem)
auto = Auto(mem)
map_data = MapData(mem)
global_data = GlobalData()
