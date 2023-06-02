import math

from common import helper
from core.game import address, mem, call
from core.game.addr import address_all


# 背包金币
def get_person_coin():
    # 背包指针 ＝ 读长整数 (读长整数 (#背包基址) ＋ #物品栏偏移)
    wpl_address = mem.read_long(mem.read_long(address_all.背包基址) + address_all.物品栏偏移)
    # 返回 (读长整数 (读长整数 (读长整数 (背包指针) － 72 ＋ 16) ＋ #数量偏移))
    return mem.read_int(mem.read_long(mem.read_long(wpl_address) - 72 + 16) + address_all.数量偏移)


# 仓库金币
def get_warehouse_coin():
    # 返回 (读长整数 (#金库金币))
    return mem.read_long(address_all.金库金币)


def get_coin_str(coin):
    coin_str = str(coin)
    if coin > 99999999:
        coin_left = coin_str[:-8]
        return coin_left + "亿"
    if coin > 9999:
        coin_left = coin_str[:-4]
        return coin_left + "万"
    return "空"


def get_role_name(self) -> str:
    """获取角色名字"""
    name_address = self.mem.read_long(address.RwName)
    name_bytes = mem.read_bytes(name_address, 200)
    return helper.unicode_to_ascii(name_bytes)


# 获取名望
def get_fame() -> int:
    rw_addr = call.person_ptr()
    return mem.read_long(rw_addr + address.RwMwAddr)


# 获取角色数量
def role_size() -> int:
    # 返回 (读整数型 (读长整数 (读长整数 (#角色基址) ＋ #角色初始指针) ＋ #角色总数偏移))
    return mem.read_int(mem.read_long(address_all.角色基址) + address_all.角色初始指针 + address_all.角色总数偏移)


# 背包地址
def get_package_address() -> int:
    # 返回 (读长整数 (读长整数 (#背包基址) ＋ #物品栏偏移) ＋ #装备栏偏移)
    return mem.read_long(mem.read_long(address_all.背包基址) + address_all.物品栏偏移) + 0x48


# 取背包物品
def back_pack_item() -> dict:
    item_addr = mem.read_long(mem.read_long(address.BbJzAddr) + address.WplPyAddr) + 72  # 物品栏偏移
    # 物品栏
    item_map = {}
    for i in range(280):
        # 物品指针 ＝ 读长整数 (物品首址 ＋ (装备索引 － 1) × 8) － 72  ' 24  装备名称=280
        equip = mem.read_long(mem.read_long(item_addr + i * 8) - 72 + 16)
        # 物品指针 ＝ 读长整数 (读长整数 (物品首址 ＋ i × 32) ＋ 16)
        if equip > 0:
            # 读整数型 (物品指针 ＋ #物品代码)
            item_code = mem.read_int(equip + address_all.物品代码)
            # 装备品级
            equip_level = mem.read_int(equip + address_all.装备品级)
            # 装备名称
            name_addr = mem.read_long(equip + address_all.物品名称)
            name = helper.unicode_to_ascii(mem.read_bytes(name_addr, 100))
            # 交易类型  1=不可交易 2=不可交易/删除 3=封装 5=账号绑定
            item_sell = mem.read_int(equip + address_all.物品交易类型)
            # 物品数量
            item_num = mem.read_int(equip + address_all.数量偏移)
            item_map[name] = equip_level, item_sell, item_num, item_code, i

    for key, value in item_map.items():
        print(key, value)

    return item_map


# 物品搜索
def search_item(item_name, item_type) -> int:
    item_map = back_pack_item()
    # 遍历所有物品
    for key, value in item_map.items():
        if key == item_name:
            print(key, value)
            equip_level, item_sell, item_num, item_code, i = value
            # 1=返回数量  2=返回物品代码 3=返回位置
            if item_type == 1:
                return item_num
            elif item_type == 2:
                return item_code
            elif item_type == 3:
                return i
    return 0


# 取角色位置
def get_role_pos() -> tuple:
    # 返回 (读整数型 (读长整数 (读长整数 (#角色基址) ＋ #角色初始指针) ＋ #普通角色位置))
    return mem.read_int(mem.read_long(address_all.角色基址) + address_all.角色初始指针 + address_all.普通角色位置),


# 取动作ID
def get_action_id() -> int:
    # 返回 (读长整数 (取人物指针 () ＋ #动作ID))
    return mem.read_long(call.person_ptr() + address_all.动作ID)


# 是否黑钻
def is_black_diamond() -> bool:
    # 返回 (读整数型 (#最大疲劳) ＞ 160)
    return mem.read_int(address_all.最大疲劳) > 160


# 实时疲劳
def get_real_fatigue() -> int:
    # 返回 (读整数型 (#最大疲劳) － 读整数型 (#当前疲劳))
    return mem.read_int(address_all.最大疲劳) - mem.read_int(address_all.当前疲劳)


# 是否菜单
def is_menu() -> bool:
    # 返回 (读整数型 (读长整数 (#游戏菜单基址) ＋ #游戏菜单偏移) ＞ 0)
    return mem.read_int(mem.read_long(5539438448) + 256) > 0


# 是否制裁
def is_punish() -> bool:
    return mem.read_long(address_all.制裁基址) == 4


# 是否安全模式
def is_safe_mode() -> bool:
    return mem.read_byte(mem.read_long(address_all.角色基址) + address_all.安全偏移) != 0


if __name__ == '__main__':
    print(get_coin_str(9000000))
