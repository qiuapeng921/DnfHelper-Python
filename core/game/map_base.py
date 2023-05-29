from common import globle
from core.game import call, address, mem, address_all


# 地图起始地址
def get_map_start_and_end():
    rw_addr = call.person_ptr()
    # 地图信息.地指针 ＝ 读长整数 (读长整数 (人物指针 ＋ #地图偏移) ＋ 16)
    map_addr = mem.read_long(mem.read_long(call.person_ptr() + address_all.地图偏移) + 16)
    # 地图信息.首地址 ＝ 读长整数 (地图信息.地指针 ＋ #地图开始2)
    start = mem.read_long(map_addr + address_all.地图开始2)
    # 地图信息.尾地址 ＝ 读长整数 (地图信息.地指针 ＋ #地图结束2)
    end = mem.read_long(map_addr + address_all.地图结束2)
    return start, end


# 获取遍历数量
def get_map_obj(start, end):
    return int((end - start) / 24)


# 基质计算
def get_address(start, obj_tmp):
    temp_addr = mem.read_long(start + obj_tmp * 24)
    return mem.read_long(temp_addr + 16) - 32


# 人物距离
def get_role_distance(person, monster) -> int:
    # x ＝ 取绝对值 (person.x － person.x)
    x = abs(person.x - monster.x)
    # y ＝ 取绝对值 (person.y － monster.y)
    y = abs(person.y - monster.y)
    # 返回 (四舍五入 (求平方根 (x × x ＋ y × y), ))
    return round(pow(x * x + y * y, 0.5))


物品校验 = 1
怪物校验 = 2
裂缝校验 = 3


# 地图是否有物品
def map_has_goods():
    return map_has_item(物品校验)


# 地图是否有怪物
def map_has_monster():
    return map_has_item(怪物校验)


def map_has_cross_hide():
    return map_has_item(裂缝校验)


# 扫描地图是否有code校验
def map_has_item(code_type):
    start, end = get_map_start_and_end()
    obj_num = get_map_obj(start, end)
    for obj_tmp in range(obj_num):
        target_addr = get_address(start, obj_tmp)
        if target_addr < 0:
            continue
        target_coordinate = read_coordinate(target_addr)

        # 类型 ＝ 读整数型 (地图信息.怪指针 ＋ #类型偏移)
        obj_type_a = mem.read_int(target_addr + address_all.类型偏移)
        # 类型B ＝ 读整数型 (地图信息.怪指针 ＋ #类型偏移 ＋ 4)
        obj_type_b = mem.read_int(target_addr + address_all.类型偏移 + 4)
        code_list = [289]
        if code_type == 1:
            if code_list.__contains__(obj_type_a) or code_list.__contains__(obj_type_b):
                return target_coordinate, target_addr
        # 地图信息.阵营 ＝ 读整数型 (地图信息.怪指针 ＋ #阵营偏移)
        obj_camp = mem.read_int(target_addr + address_all.阵营偏移)
        # 地图信息.代码 ＝ 读整数型 (地图信息.怪指针 ＋ #代码偏移)
        obj_code = mem.read_int(target_addr + address_all.代码偏移)

        success_code_a = [529, 545, 273, 61440]
        success_code_b = [529, 545, 273, 61440]

        if obj_camp == 0 or target_addr == call.person_ptr():
            continue
        if code_type == 2:
            fail_code = [258, 889, 63821, 818, 799, 407000719, 109006953, 407000719, 109007006, 10624]
            if fail_code.__contains__(obj_code) or obj_camp == 0:
                continue

            if success_code_a.__contains__(obj_type_a) or success_code_b.__contains__(obj_type_b) and obj_camp > 0:
                return target_coordinate, target_addr
        if code_type == 3:
            if obj_code == 490019076:
                return target_coordinate, target_addr
    return None, 0


def read_coordinate(param: int) -> globle.CoordinateType:
    """读取坐标"""
    coordinate = globle.CoordinateType()
    if mem.read_int(param + address_all.类型偏移) == 273:
        ptr = mem.read_long(param + address_all.读取坐标)
        coordinate.x = int(mem.read_float(ptr + 0))
        coordinate.y = int(mem.read_float(ptr + 4))
        coordinate.z = int(mem.read_float(ptr + 8))
    else:
        ptr = mem.read_long(param + address_all.方向偏移)
        coordinate.x = int(mem.read_float(ptr + 32))
        coordinate.y = int(mem.read_float(ptr + 36))
        coordinate.z = int(mem.read_float(ptr + 40))

    return coordinate
