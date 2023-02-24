from game.structure import CoordinateType, GameMapType


class GameMap:
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
        fxArr = []
        fxJh = [
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
                fxArr[i] = fxJh[tx][i]
        else:
            for i in range(3):
                fxArr[i] = 0

        if fxArr[fx] == 1:
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
    def gen_map(cls, width: int, height: int, map_channel: list, game_map: [[[GameMapType]]]) -> [[GameMapType]]:
        game_map = [[GameMapType] * 10]
        for x in range(width):
            game_map[x] = [GameMapType] * height

        i, x, y = (0, 0, 0)
        for y in range(height):
            for x in range(width):
                game_map[x][y].MapCoordinates.X = x
                game_map[x][y].MapCoordinates.Y = y
                game_map[x][y].MapChannel = map_channel[i]
                game_map[x][y].Left = cls.judge_direction(map_channel[i], 0)
                game_map[x][y].Right = cls.judge_direction(map_channel[i], 1)
                game_map[x][y].Up = cls.judge_direction(map_channel[i], 2)
                game_map[x][y].Down = cls.judge_direction(map_channel[i], 3)
                game_map[x][y].BackgroundColor = 0xFFFFFF
                i = i + 1
                if game_map[x][y].MapChannel == 0:
                    game_map[x][y].BackgroundColor = 0x000000

        return game_map
