# 坐标结构
class CoordinateType:
    X, Y, Z = (0, 0, 0)


# 地图数据
class MapDataType:
    MapName = ""  # 地图名称
    MapNum = 0  # 地图编号
    MapChannel = []  # 地图通道
    StartZb = CoordinateType  # 起始坐标
    EndZb = CoordinateType  # 终点坐标
    Width = 0  # 宽
    Height = 0  # 高
    MapRoute = []  # 地图走法
    ConsumeFatigue = 0  # 消耗疲劳
    ChannelNum = 0  # 通道数量
    Tmp = 0  # 临时变量


# 游戏地图
class GameMapType:
    MapCoordinates = CoordinateType
    Left = False  # 地图左边
    Right = False  # 地图右边
    Up = False  # 地图上边
    Down = False  # 地图下边
    MapChannel = 0  # 地图通道
    BackgroundColor = 0  # 背景颜色


# 地图节点
class MapNodeType:
    F = 0  # 地图F点
    G = 0  # 地图G点
    H = 0  # 地图H点
    CurrentCoordinates = CoordinateType  # 当前坐标
    FinalCoordinates = CoordinateType  # 最终坐标


# 全局数据
class GlobalData:
    def __init__(self):
        # 自动开关
        self.auto_switch = False
        # 任务编号
        self.task_id = 0
        # 副本编号
        self.map_id = 0
        # 副本难度
        self.map_level = 0
        # 角色总数
        self.role_count = 0
