# 坐标结构
class CoordinateType:
    def __init__(self):
        self.X = 0
        self.Y = 0
        self.Z = 0


# 地图数据
class MapDataType:
    def __init__(self):
        self.MapName = ""  # 地图名称
        self.MapNum = 0  # 地图编号
        self.MapChannel = []  # 地图通道
        self.StartZb = CoordinateType  # 起始坐标
        self.EndZb = CoordinateType  # 终点坐标
        self.Width = 0  # 宽
        self.Height = 0  # 高
        self.MapRoute = []  # 地图走法 []CoordinateType
        self.ConsumeFatigue = 0  # 消耗疲劳
        self.ChannelNum = 0  # 通道数量
        self.Tmp = 0  # 临时变量


# 游戏地图
class GameMapType:
    def __init__(self):
        self.MapCoordinates = CoordinateType  # 地图坐标
        self.Left = False  # 地图左边
        self.Right = False  # 地图右边
        self.Up = False  # 地图上边
        self.Down = False  # 地图下边
        self.MapChannel = 0  # 地图通道
        self.BackgroundColor = 0  # 背景颜色


# 地图节点
class MapNodeType:
    def __init__(self):
        self.F = 0  # 地图F点
        self.G = 0  # 地图G点
        self.H = 0  # 地图H点
        self.CurrentCoordinates = CoordinateType  # 当前坐标
        self.FinalCoordinates = CoordinateType  # 最终坐标


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
