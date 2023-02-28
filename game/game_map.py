from typing import Type

from common import mem
from game import address
from game.map_data import MapData
from game.structure import CoordinateType, GameMapType, MapDataType


class GameMap:

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def get_direction(cls, cut_room: CoordinateType, next_room: CoordinateType) -> int:
        """获取方向"""
        direction = 0
        x = cut_room.x - next_room.x
        y = cut_room.y - next_room.y
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
                y_data.map_coordinates.x = x
                y_data.map_coordinates.y = y
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
    def map_data(cls) -> Type[MapDataType]:
        """地图数据"""
        map_obj = MapData(mem)

        data = MapDataType

        room_data = mem.read_long(mem.read_long(mem.read_long(address.FJBHAddr) + address.SJAddr) + address.MxPyAddr)
        room_index = map_obj.decode(room_data + address.SyPyAddr)

        data.Width = mem.read_int(mem.read_long(room_data + address.KgPyAddr) + room_index * 8 + 0)
        data.Height = mem.read_int(mem.read_long(room_data + address.KgPyAddr) + room_index * 8 + 4)
        data.Tmp = mem.read_long(mem.read_long(room_data + address.SzPyAddr) + 32 * room_index + 8)
        data.ChannelNum = data.Width * data.Height

        for i in range(len(data.ChannelNum)):
            data.map_channel.insert(0 + i, mem.read_int(data.Tmp + i * 4))

        data.start_zb.x = map_obj.get_cut_room().x + 1
        data.start_zb.y = map_obj.get_cut_room().y + 1
        data.end_zb.x = map_obj.get_boss_room().x + 1
        data.end_zb.y = map_obj.get_boss_room().y + 1

        if data.start_zb.x == data.end_zb.x and data.start_zb.y == data.end_zb.y:
            return data

        data.ConsumeFatigue = cls.get_route(data.map_channel, data.Width, data.Height, data.start_zb, data.end_zb,
                                            data.map_route)
        return data

    @classmethod
    def get_route(cls, map_channel: [], width: int, height: int, map_start: CoordinateType, map_end: CoordinateType,
                  reality_route: [CoordinateType]) -> int:
        """获取走法"""
        start_coordinate = CoordinateType
        end_coordinate = CoordinateType

        map_flag = [[]]
        map_array = [[]]
        cross_way = [[]]

        if map_start.x == map_end.x and map_start.y == map_end.y:
            return 0

        map_array = cls.gen_map(width, height, map_channel, map_array)
        map_flag = cls.display_map(map_array, width, height, map_flag)
        start_coordinate.X = map_start.x * 3 - 2
        start_coordinate.Y = map_start.y * 3 - 2
        end_coordinate.X = map_end.x * 3 - 2
        end_coordinate.Y = map_end.y * 3 - 2
        cls.route_calculate(map_flag, start_coordinate, end_coordinate, width * 3, height * 3, cross_way)
        return cls.tidy_coordinate(cross_way, reality_route)

    @classmethod
    def display_map(cls, map_arr: [[GameMapType]], width: int, height: int, map_label: [[GameMapType]]) -> [
        [GameMapType]]:
        """显示地图"""
        map_label = [[GameMapType]] * 3
        for x in range(width * 3):
            map_label[x] = [GameMapType] * height * 3

        for y in range(height):
            for x in range(width):
                map_label[(x + 1) * 3 - 2][(y + 1) * 3 - 2].background_color = 0xFFFFFF
                if map_arr[x][y].Left:
                    map_label[(x + 1) * 3 - 3][(y + 1) * 3 - 2].background_color = 0xFFFFFF
                if map_arr[x][y].Right:
                    map_label[(x + 1) * 3 - 1][(y + 1) * 3 - 2].background_color = 0xFFFFFF
                if map_arr[x][y].Up:
                    map_label[(x + 1) * 3 - 2][(y + 1) * 3 - 3].background_color = 0xFFFFFF
                if map_arr[x][y].Down:
                    map_label[(x + 1) * 3 - 2][(y + 1) * 3 - 1].background_color = 0xFFFFFF

        return map_arr

    @classmethod
    def route_calculate(cls, a, b, c, d, e, f) -> int:
        """路径计算"""
        pass
