from common import globle
from core.game import call, address, mem
from core.game.addr import address_all


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
        if start == target_addr:
            continue
        # 地图信息.阵营 ＝ 读整数型 (地图信息.怪指针 ＋ #阵营偏移)
        obj_camp = mem.read_int(target_addr + address_all.阵营偏移)
        if obj_camp <= 0:
            continue
        # 如果是地图固定坐标 则跳过
        # 怪物代码 ＝ 读整数型 (地图信息.怪指针 ＋ #代码偏移)
        obj_code = mem.read_int(target_addr + address_all.代码偏移)
        if check_monster(obj_code):
            continue
        # 怪物位置
        target_coordinate = read_coordinate(target_addr)

        # 类型 ＝ 读整数型 (地图信息.怪指针 ＋ #类型偏移)
        obj_type_a = mem.read_int(target_addr + address_all.类型偏移)
        # 类型B ＝ 读整数型 (地图信息.怪指针 ＋ #类型偏移 ＋ 4)
        obj_type_b = mem.read_int(target_addr + address_all.类型偏移 + 4)
        code_list = [289]
        if code_type == 1:
            if code_list.__contains__(obj_type_a) or code_list.__contains__(obj_type_b):
                return target_coordinate, target_addr

        monster_code = [529, 545, 273, 61440]
        if obj_camp == 0 or target_addr == call.person_ptr():
            continue
        if code_type == 2:
            fail_code = [258, 889, 63821, 818, 799, 407000719, 109006953, 407000719, 109007006, 10624]
            if fail_code.__contains__(obj_code) or obj_camp == 0:
                continue

            if monster_code.__contains__(obj_type_a) or monster_code.__contains__(obj_type_b):
                return target_coordinate, target_addr
        if code_type == 3:
            if obj_code == 490019076:
                return target_coordinate, target_addr
    return None, 0


# 地图固定坐标
def check_monster(monster):
    if monster == 109013676:
        return True
    elif monster == 109051364:  # 风暴格兰迪柱子1
        return True
    elif monster == 109051365:  # 风暴格兰迪柱子2
        return True
    elif monster == 109051366:  # 风暴格兰迪柱子3
        return True
    elif monster == 109000441:  # 破坏通讯器 不幸之门 旋转木桩
        return True
    elif monster == 109010714:  # 无底坑道 谎言基尔施
        return True
    elif monster == 109010715:  # 无底坑道 锐利的卡沙萨
        return True
    elif monster == 10624:  # 破坏实验装置 发电机
        return True
    elif monster == 8104:  # 哥布林投石车
        return True
    elif monster == 109034881:  # 蕴含时空石的建筑
        return True
    elif monster == 69268:  # 剧情的建筑 暴君的祭坛地图
        return True
    elif monster == 85157:  # 克雷发电机控制开关
        return True
    elif monster == 85159:  # 克雷发电机
        return True
    elif monster == 10199:  # 破损的GT-9600
        return True
    elif monster == 8824:  # 解救冒险家被抓 根特外围关人笼子
        return True
    elif monster == 817:  # 冻结之月亮
        return True
    elif monster == 109022849:  # 大奴隶
        return True
    elif monster == 80416:  # '
        return True
    elif monster == 80417:  # 发电机 拯救皇女陛下领主房间
        return True
    elif monster == 80369:  # 青铜石巨人的子弹
        return True
    elif monster == 69037:  # 巨龙石像
        return True
    elif monster == 61320:  # 稻草人
        return True
    elif monster == 61321:  # 狂风稻草人
        return True
    elif monster == 13097:  # 狂风稻草人
        return True
    elif monster == 1087:  # 狂风稻草人
        return True
    elif monster == 109010180:  # 狂风稻草人
        return True
    else:
        return False

# 获取坐标位置
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


# 取当前房间
def get_current_room():
    coordinate = globle.CoordinateType()
    # 房间数据 ＝ 读长整数 (读长整数 (读长整数 (#房间编号) ＋ #时间基址) ＋ #门型偏移)
    room_data = mem.read_long(
        mem.read_long(mem.read_long(address_all.房间编号) + address_all.时间基址) + address_all.门型偏移)
    # 返回数据.x ＝ 读长整数 (房间数据 ＋ #当前房间X)
    coordinate.x = mem.read_long(room_data + address_all.当前房间X)
    # 返回数据.y ＝ 读长整数 (房间数据 ＋ #当前房间Y)
    coordinate.y = mem.read_long(room_data + address_all.当前房间Y)
    return coordinate
