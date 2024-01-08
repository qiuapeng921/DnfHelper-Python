cmd = "cmd"

win_app = None


# 全局数据
class GlobalData:
    # 自动开关
    auto_switch = False
    # 任务编号
    task_id = 0
    # 副本编号
    map_id = 0
    # 副本难度
    map_level = 0
    # 角色总数
    role_count = 0
    # 完成角色
    completed_role = 0


# 坐标结构
class CoordinateType:
    x, y, z = (0, 0, 0)

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0


# 地图数据
class MapDataType:
    map_name = ""  # 地图名称
    map_um = 0  # 地图编号
    map_channel = [int]  # 地图通道
    start_zb = CoordinateType()  # 起始坐标
    end_zb = CoordinateType()  # 终点坐标
    width = 0  # 宽
    height = 0  # 高
    map_route = []  # 地图走法
    consume_fatigue = 0  # 消耗疲劳
    channel_num = 0  # 通道数量
    tmp = 0  # 临时变量

    def __init__(self):
        self.map_name = ""
        self.map_um = 0
        self.map_channel = []
        self.start_zb = CoordinateType()
        self.end_zb = CoordinateType()
        self.width = 0
        self.height = 0
        self.map_route = []
        self.consume_fatigue = 0
        self.channel_num = 0
        self.tmp = 0


# 游戏地图
class GameMapType:
    map_coordinates = CoordinateType()  # 地图坐标
    left = False  # 地图左边
    right = False  # 地图右边
    up = False  # 地图上边
    down = False  # 地图下边
    map_channel = 0  # 地图通道
    background_color = 0  # 背景颜色

    def __init__(self):
        self.map_coordinates = CoordinateType()
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.map_channel = 0
        self.background_color = 0


# 地图节点
class MapNodeType:
    f = 0  # 地图F点
    g = 0  # 地图G点
    h = 0  # 地图H点
    current_coordinates = CoordinateType()  # 当前坐标
    final_coordinates = CoordinateType()  # 最终坐标

    def __init__(self):
        self.f = 0
        self.g = 0
        self.h = 0
        self.current_coordinates = CoordinateType()
        self.final_coordinates = CoordinateType()


class MapTraversalType:
    rw_addr = 0  # 地图地址
    map_data = 0  # 地图数据
    start = 0  # 起始位置
    end = 0  # 结束位置
    obj_num = 0  # 物体数量
    obj_tmp = 0  # 物体临时变量
    obj_ptr = 0  # 物体指针
    obj_camp = 0  # 物体阵营
    obj_blood = 0  # 物体血量
    obj_type_a = 0  # 物体类型A
    obj_type_b = 0  # 物体类型B
    obj_code = 0  # 物体代码
    obj_name_a = ""  # 物体名称A
    obj_name_b = ""  # 物体名称B
    rw_coordinate = CoordinateType()  # 地图坐标类型
    gw_coordinate = CoordinateType()  # 游戏坐标类型
    wp_coordinate = CoordinateType()  # 终点坐标类型

    def __init__(self):
        # 地图遍历类型的属性
        self.rw_addr = 0
        self.map_data = 0
        self.start = 0
        self.end = 0
        self.obj_num = 0
        self.obj_tmp = 0
        self.obj_ptr = 0
        self.obj_camp = 0
        self.obj_blood = 0
        self.obj_type_a = 0
        self.obj_type_b = 0
        self.obj_code = 0
        self.obj_name_a = ""
        self.obj_name_b = ""
        self.rw_coordinate = CoordinateType()
        self.gw_coordinate = CoordinateType()
        self.wp_coordinate = CoordinateType()
