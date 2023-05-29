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


# 地图是否有物品
def map_has_goods():
    return map_has_item(1)


# 地图是否有怪物
def map_has_monster():
    return map_has_item(2)


# 扫描地图是否有code校验 1 物品校验 2怪物校验
def map_has_item(code_type):
    start, end = get_map_start_and_end()
    obj_num = get_map_obj(start, end)
    for obj_tmp in range(obj_num):
        target_addr = get_address(start, obj_tmp)
        if target_addr < 0:
            continue
        # 类型 ＝ 读整数型 (地图信息.怪指针 ＋ #类型偏移)
        obj_type_a = mem.read_int(target_addr + address_all.类型偏移)
        # 类型B ＝ 读整数型 (地图信息.怪指针 ＋ #类型偏移 ＋ 4)
        obj_type_b = mem.read_int(target_addr + address_all.类型偏移 + 4)
        code_list = [289]
        if code_type == 1:
            if code_list.__contains__(obj_type_a) or code_list.__contains__(obj_type_b):
                return True
        # 地图信息.阵营 ＝ 读整数型 (地图信息.怪指针 ＋ #阵营偏移)
        obj_camp = mem.read_int(target_addr + address_all.阵营偏移)
        # 地图信息.代码 ＝ 读整数型 (地图信息.怪指针 ＋ #代码偏移)
        obj_code = mem.read_int(target_addr + address_all.代码偏移)
        if code_type == 2:
            fail_code = [258, 889, 63821, 818, 799, 407000719, 109006953, 407000719, 109007006, 10624]
            if fail_code.__contains__(obj_code) or obj_camp == 0:
                continue
            success_code = [529, 545, 273, 61440]
            if success_code.__contains__(obj_code):
                return True
    return False
