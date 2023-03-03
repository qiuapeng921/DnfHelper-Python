# 坐标结构
class CoordinateType:
    x, y, z = (0, 0, 0)


# 地图数据
class MapDataType:
    map_name = ""  # 地图名称
    map_um = 0  # 地图编号
    map_channel = []  # 地图通道
    start_zb = CoordinateType  # 起始坐标
    end_zb = CoordinateType  # 终点坐标
    width = 0  # 宽
    height = 0  # 高
    map_route = []  # 地图走法
    consume_fatigue = 0  # 消耗疲劳
    channel_num = 0  # 通道数量
    tmp = 0  # 临时变量


# 游戏地图
class GameMapType:
    map_coordinates = CoordinateType  # 地图坐标
    left = False  # 地图左边
    right = False  # 地图右边
    up = False  # 地图上边
    down = False  # 地图下边
    map_channel = 0  # 地图通道
    background_color = 0  # 背景颜色


# 地图节点
class MapNodeType:
    f = 0  # 地图F点
    g = 0  # 地图G点
    h = 0  # 地图H点
    current_coordinates = CoordinateType  # 当前坐标
    final_coordinates = CoordinateType  # 最终坐标


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


# 地图遍历
class Traversal:
    rw_addr = 0  # 人物地址
    map_data = 0  # 地图数据
    start = 0  # 首部地址
    end = 0  # 尾部地址
    obj_num = 0  # 对象数量
    obj_tmp = 0  # 对象变量
    obj_ptr = 0  # 对象指针
    obj_camp = 0  # 对象阵营
    obj_blood = 0  # 对象血量
    obj_type_a = 0  # 对象类型A
    obj_type_b = 0  # 对象类型B
    obj_code = 0  # 对象代码
    obj_name_a = ""  # 对象名称
    obj_name_b = ""  # 物品名称
    rw_coordinate = CoordinateType  # 人物坐标
    gw_coordinate = CoordinateType  # 怪物坐标
    wp_coordinate = CoordinateType  # 物品坐标
