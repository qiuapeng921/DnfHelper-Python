# 坐标结构
class CoordinateType:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0


class GlobalData:
    def __init__(self):
        # 自动开关
        auto_switch = bool
        # 任务编号
        self.task_id = 0
        # 副本编号
        self.map_id = 0
        # 副本难度
        self.map_level = 0
        # 角色总数
        self.role_count = 0
