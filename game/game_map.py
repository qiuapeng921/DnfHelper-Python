from typing import Type

from common import mem
from game import address
from game.map_data import MapData
from game.structure import CoordinateType, GameMapType, MapDataType


class GameMap:
    map_data = MapData

    def __init__(self):
        self.map_data = MapData(mem)

    @classmethod
    def get_direction(cls, cut_room: CoordinateType, next_room: CoordinateType) -> int:
        """获取方向"""
        direction = 0
        x = cut_room.X - next_room.X
        y = cut_room.Y - next_room.Y
        if x == 0 and y == 0:
            return 4
        if x == 0:
            if y == 1:
                direction = 2
            else:
                direction = 3
        elif y == 0:
            if x == 1:
                direction = 0
            else:
                direction = 1
        return direction

    @classmethod
    def judge_direction(cls, tx: int, fx: int) -> bool:
        """寻路_判断方向"""
        # 方向数组
        direction_arr = []
        # 方向集合
        direction_set = [
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 1, 0],
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [1, 0, 1, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 1],
            [0, 1, 0, 1],
            [0, 0, 1, 1],
            [0, 1, 1, 1],
            [1, 0, 0, 1],
            [1, 1, 0, 1],
            [1, 0, 1, 1],
            [1, 1, 1, 1],
        ]
        if fx <= 15:
            for i in range(3):
                direction_arr[i] = direction_set[tx][i]
        else:
            for i in range(3):
                direction_arr[i] = 0

        if direction_arr[fx] == 1:
            return True

        return False

    @classmethod
    def tidy_coordinate(cls, simulation_route: [CoordinateType], reality_route: [CoordinateType]):
        """
        整理坐标
        :param simulation_route:
        :param reality_route:
        :return:
        """
        x, y, k = (0, 0, 0)
        temp_coordinates = CoordinateType
        for i in range(len(simulation_route)):
            x = (simulation_route[i].X + 2) % 3
            y = (simulation_route[i].Y + 2) % 3
            if x == 0 and y == 0:
                temp_coordinates.X = (simulation_route[i].X + 2) / 3 - 1
                temp_coordinates.Y = (simulation_route[i].Y + 2) / 3 - 1
                # 参_真实走法.insert(参_真实走法.begin() + k, 局_临时坐标);
                reality_route.insert(0 + k, temp_coordinates)
                k = k + 1

        return k, reality_route

    @classmethod
    def gen_map(cls, width: int, height: int, map_channel: list, game_map):
        """生成地图"""
        i, x, y = (0, 0, 0)
        for x in range(width):
            y_game_map = []
            for y in range(height):
                y_data = GameMapType
                y_data.MapCoordinates.X = x
                y_data.MapCoordinates.Y = y
                y_data.MapChannel = map_channel[i]
                y_data.Left = cls.judge_direction(map_channel[i], 0)
                y_data.Right = cls.judge_direction(map_channel[i], 1)
                y_data.Up = cls.judge_direction(map_channel[i], 2)
                y_data.Down = cls.judge_direction(map_channel[i], 3)
                y_data.BackgroundColor = 0xFFFFFF
                i = i + 1
                if y_data.MapChannel == 0:
                    y_data.BackgroundColor = 0x000000

                y_game_map.insert(y, y_data)

            game_map.insert(x, y_game_map)

        return game_map

    @classmethod
    def MapData(cls) -> Type[MapDataType]:
        """地图数据"""
        mapData = MapDataType

        roomData = mem.read_long(mem.read_long(mem.read_long(address.FJBHAddr) + address.SJAddr) + address.MxPyAddr)
        roomIndex = cls.map_data.decode(roomData + address.SyPyAddr)

        mapData.Width = mem.read_int(mem.read_long(roomData + address.KgPyAddr) + roomIndex * 8 + 0)
        mapData.Height = mem.read_int(mem.read_long(roomData + address.KgPyAddr) + roomIndex * 8 + 4)
        mapData.Tmp = mem.read_long(mem.read_long(roomData + address.SzPyAddr) + 32 * roomIndex + 8)
        mapData.ChannelNum = mapData.Width * mapData.Height

        for i in range(len(mapData.ChannelNum)):
            mapData.MapChannel.insert(0 + i, mem.read_int(mapData.Tmp + i * 4))

        mapData.StartZb.X = cls.map_data.get_cut_room().X + 1
        mapData.StartZb.Y = cls.map_data.get_cut_room().Y + 1
        mapData.EndZb.X = cls.map_data.get_boss_room().X + 1
        mapData.EndZb.Y = cls.map_data.get_boss_room().Y + 1

        if mapData.StartZb.X == mapData.EndZb.X and mapData.StartZb.Y == mapData.EndZb.Y:
            return mapData

        mapData.ConsumeFatigue = cls.get_route(mapData.MapChannel, mapData.Width, mapData.Height, mapData.StartZb,
                                               mapData.EndZb, mapData.MapRoute)
        return mapData

    @classmethod
    def get_route(cls, a, b, c, d, e, f) -> int:
        """获取走法"""
        pass

    @classmethod
    def display_map(cls, a, b, c, d, e, f) -> int:
        """显示地图"""
        pass

    @classmethod
    def route_calculate(cls, a, b, c, d, e, f) -> int:
        """路径计算"""
        pass
