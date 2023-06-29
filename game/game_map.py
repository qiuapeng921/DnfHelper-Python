from common import globle
from game import mem
from game import address
from game.map_data import MapData


class GameMap:

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def get_direction(cls, cut_room, next_room):
        """
        获取方向
        :param cut_room
        :param next_room
        :return: int
        """
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
    def judge_direction(cls, tx, fx):
        """
        寻路_判断方向
        :param tx: int
        :param fx: int
        :return: bool
        """
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
            for i in range(4):
                direction_arr.insert(i, direction_set[tx][i])
        else:
            for i in range(4):
                direction_arr.insert(i, 0)

        if direction_arr[fx] == 1:
            return True

        return False

    @classmethod
    def tidy_coordinate(cls, simulation_route, reality_route):
        """
        整理坐标
        :param simulation_route: [CoordinateType]
        :param reality_route: [CoordinateType]
        :return: (int, [CoordinateType])
        """
        x, y, k = (0, 0, 0)
        for i in range(len(simulation_route)):
            temp_coordinates = globle.CoordinateType()
            x = (simulation_route[i].x + 2) % 3
            y = (simulation_route[i].y + 2) % 3
            if x == 0 and y == 0:
                temp_coordinates.x = int((simulation_route[i].x + 2) / 3 - 1)
                temp_coordinates.y = int((simulation_route[i].y + 2) / 3 - 1)
                reality_route.insert(0 + k, temp_coordinates)
                k = k + 1

        return k, reality_route

    @classmethod
    def gen_map(cls, width, height, map_channel):
        """
        生成地图
        :param width: int
        :param height: int
        :param map_channel: [int]
        :return: [[GameMapType]]
        """
        game_map = [[globle.GameMapType()] for _ in range(width)]
        for x in range(width):
            game_map[x] = [globle.GameMapType() for _ in range(height)]

        i = 0
        for y in range(height):
            for x in range(width):
                game_map[x][y].map_coordinates.x = x
                game_map[x][y].map_coordinates.y = y
                game_map[x][y].map_channel = map_channel[i]
                game_map[x][y].left = cls.judge_direction(map_channel[i], 0)
                game_map[x][y].right = cls.judge_direction(map_channel[i], 1)
                game_map[x][y].up = cls.judge_direction(map_channel[i], 2)
                game_map[x][y].down = cls.judge_direction(map_channel[i], 3)
                game_map[x][y].background_color = 0xFFFFFF
                i = i + 1
                if game_map[x][y].map_channel == 0:
                    game_map[x][y].background_color = 0x000000

        return game_map

    @classmethod
    def map_data(cls) -> globle.MapDataType:
        """地图数据"""
        map_obj = MapData(mem)
        data = globle.MapDataType()

        room_data = mem.read_long(mem.read_long(mem.read_long(address.FJBHAddr) + address.SJAddr) + address.MxPyAddr)
        room_index = map_obj.decode(room_data + address.SyPyAddr)

        data.width = mem.read_int(mem.read_long(room_data + address.KgPyAddr) + room_index * 8 + 0)
        data.height = mem.read_int(mem.read_long(room_data + address.KgPyAddr) + room_index * 8 + 4)
        data.tmp = mem.read_long(mem.read_long(room_data + address.SzPyAddr) + 32 * room_index + 8)
        data.channel_num = data.width * data.height

        for i in range(data.channel_num):
            data.map_channel.insert(0 + i, mem.read_int(data.tmp + i * 4))

        data.start_zb.x = map_obj.get_cut_room().x + 1
        data.start_zb.y = map_obj.get_cut_room().y + 1
        data.end_zb.x = map_obj.get_boss_room().x + 1
        data.end_zb.y = map_obj.get_boss_room().y + 1

        if data.start_zb.x == data.end_zb.x and data.start_zb.y == data.end_zb.y:
            return data

        data.consume_fatigue = cls.get_route(data.map_channel, data.width, data.height, data.start_zb, data.end_zb,
                                             data.map_route)
        return data

    @classmethod
    def get_route(cls, map_channel, width, height, map_start, map_end, reality_route):
        """
        获取走法
        :param map_channel: [int]
        :param width: int
        :param height: int
        :param map_start: CoordinateType
        :param map_end: CoordinateType
        :param reality_route: [CoordinateType]
        :return: (int, [[CoordinateType]])
        """
        start_coordinate = globle.CoordinateType()
        end_coordinate = globle.CoordinateType()

        if map_start.x == map_end.x and map_start.y == map_end.y:
            return 0, None

        map_array = cls.gen_map(width, height, map_channel)
        map_flag = cls.display_map(map_array, width, height)
        start_coordinate.x = map_start.x * 3 - 2
        start_coordinate.y = map_start.y * 3 - 2
        end_coordinate.x = map_end.x * 3 - 2
        end_coordinate.y = map_end.y * 3 - 2
        cross_way = cls.route_calculate(map_flag, start_coordinate, end_coordinate, width * 3, height * 3)
        return cls.tidy_coordinate(cross_way, reality_route)

    @classmethod
    def display_map(cls, map_arr, width, height):
        """
        显示地图
        :param map_arr: [[GameMapType]]
        :param width: int
        :param height: int
        :return: [[GameMapType]]
        """
        map_label = [[globle.GameMapType()] for _ in range(width * 3)]
        for x in range(width * 3):
            map_label[x] = [globle.GameMapType() for _ in range(height * 3)]

        for y in range(height):
            for x in range(width):
                map_label[(x + 1) * 3 - 2][(y + 1) * 3 - 2].background_color = 0xFFFFFF
                if map_arr[x][y].left:
                    map_label[(x + 1) * 3 - 3][(y + 1) * 3 - 2].background_color = 0xFFFFFF
                if map_arr[x][y].right:
                    map_label[(x + 1) * 3 - 1][(y + 1) * 3 - 2].background_color = 0xFFFFFF
                if map_arr[x][y].up:
                    map_label[(x + 1) * 3 - 2][(y + 1) * 3 - 3].background_color = 0xFFFFFF
                if map_arr[x][y].down:
                    map_label[(x + 1) * 3 - 2][(y + 1) * 3 - 1].background_color = 0xFFFFFF

        return map_label

    @classmethod
    def route_calculate(cls, map_label, map_start, map_end, width, height):
        """
        路径计算
        :param map_label: [[GameMapType]]
        :param map_start: CoordinateType
        :param map_end: CoordinateType
        :param width: int
        :param height: int
        :return: [CoordinateType]
        """
        tmp_node = globle.MapNodeType()  # 待检测节点, 临时节点
        open_list = list()  # 开放列表
        close_list = list()  # 关闭列表

        short_est_num = 0  # 最短编号

        tmp_node.current_coordinates.x = map_start.x
        tmp_node.current_coordinates.y = map_start.y

        map_label[map_start.x][map_start.y].background_color = 0x00FF00
        map_label[map_start.x][map_start.y].background_color = 0x0000FF
        open_list.insert(0, tmp_node)

        move_arr = []

        while True:
            min_f = 0
            for y in range(len(open_list)):
                if min_f == 0:
                    min_f = open_list[0].f
                    short_est_num = y
                if open_list[y].f < min_f:
                    min_f = open_list[y].f
                    short_est_num = y

            tmp_node = open_list[short_est_num]
            open_list.pop(0 + short_est_num)
            close_list.insert(0, tmp_node)

            if tmp_node.current_coordinates.x != map_start.x or tmp_node.current_coordinates.y != map_start.y:
                if tmp_node.current_coordinates.x != map_end.x or tmp_node.current_coordinates.y != map_end.y:
                    map_label[tmp_node.current_coordinates.x][
                        tmp_node.current_coordinates.y].background_color = 0x0080FF

            for y in range(len(close_list)):
                if close_list[y].current_coordinates.x == map_end.x and close_list[
                    y].current_coordinates.y == map_end.y:
                    wait_handle_node = close_list[y]
                    while True:
                        for x in range(len(close_list)):
                            if close_list[x].current_coordinates.x == wait_handle_node.final_coordinates.x and \
                                    close_list[x].current_coordinates.y == wait_handle_node.final_coordinates.y:
                                wait_handle_node = close_list[x]
                                break
                        if wait_handle_node.current_coordinates.x != map_start.x or wait_handle_node.current_coordinates.y != map_start.y:
                            map_label[wait_handle_node.current_coordinates.x][
                                wait_handle_node.current_coordinates.y].background_color = 0x00D8D8
                            move_arr.insert(0, wait_handle_node.current_coordinates)

                        if wait_handle_node.current_coordinates.x == map_start.x and wait_handle_node.current_coordinates.y == map_start.y:
                            break
                    move_arr.insert(0, map_start)
                    move_arr.append(map_end)
                    return move_arr
            for y in range(4):
                wait_handle_coordinate = globle.CoordinateType()  # 待检测坐标
                if y == 0:
                    wait_handle_coordinate.x = tmp_node.current_coordinates.x
                    wait_handle_coordinate.y = tmp_node.current_coordinates.y - 1
                elif y == 1:
                    wait_handle_coordinate.x = tmp_node.current_coordinates.x - 1
                    wait_handle_coordinate.y = tmp_node.current_coordinates.y
                elif y == 2:
                    wait_handle_coordinate.x = tmp_node.current_coordinates.x + 1
                    wait_handle_coordinate.y = tmp_node.current_coordinates.y
                else:
                    wait_handle_coordinate.x = tmp_node.current_coordinates.x
                    wait_handle_coordinate.y = tmp_node.current_coordinates.y + 1
                if wait_handle_coordinate.x < 0 or wait_handle_coordinate.x > (
                        width - 1) or wait_handle_coordinate.y < 0 or wait_handle_coordinate.y > (height - 1):
                    continue
                if map_label[wait_handle_coordinate.x][wait_handle_coordinate.y].background_color == 0x000000:
                    continue
                exist_close_list = False
                for x in range(len(close_list)):
                    if close_list[x].current_coordinates.x == wait_handle_coordinate.x and close_list[
                        x].current_coordinates.y == wait_handle_coordinate.y:
                        exist_close_list = True
                        break
                if exist_close_list:
                    continue
                exist_open_list = False
                for x in range(len(open_list)):
                    if open_list[x].current_coordinates.x == wait_handle_coordinate.x and open_list[
                        x].current_coordinates.y == wait_handle_coordinate.y:
                        if wait_handle_coordinate.x != tmp_node.current_coordinates.x or wait_handle_coordinate.y != tmp_node.current_coordinates.y:
                            guess_g = 14
                        else:
                            guess_g = 10

                        if tmp_node.g + guess_g < open_list[x].g:
                            open_list[x].final_coordinates = tmp_node.current_coordinates

                        exist_open_list = True
                        break
                if not exist_open_list:
                    if wait_handle_coordinate.x == tmp_node.current_coordinates.x or wait_handle_coordinate.y == tmp_node.current_coordinates.y:
                        guess_g = 10
                    else:
                        guess_g = 14
                    wait_handle_node = globle.MapNodeType()
                    wait_handle_node.g = tmp_node.g + guess_g
                    wait_handle_node.h = map_end.x - wait_handle_coordinate.x * 10 + map_end.y - wait_handle_coordinate.y * 10
                    wait_handle_node.f = wait_handle_node.g + wait_handle_node.h
                    wait_handle_node.current_coordinates = wait_handle_coordinate
                    wait_handle_node.final_coordinates = tmp_node.current_coordinates
                    open_list.insert(0, wait_handle_node)
            if len(open_list) == 0:
                break
