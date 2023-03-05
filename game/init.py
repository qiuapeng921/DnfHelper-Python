"""
初始化全局变量
"""

from common import globle
from game import auto, map_data,game_map, mem, map_traversal, pack

auto = auto.Auto(mem)
traversal = map_traversal.Screen()
map_data = map_data.MapData(mem)
game_map = game_map.GameMap()
global_data = globle.GlobalData()
pack = pack.Pack()
