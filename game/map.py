from common import mem
from game import map_data, call, structure, address


def full_screen():
    """全屏遍历"""
    map_obj = map_data.MapData(mem)
    if map_obj.get_stat() is not 3:
        return

    data = structure.Traversal()
    data.rw_addr = call.person_ptr()
    data.MapData = mem.read_long(mem.read_long(data.rw_addr + address.DtPyAddr) + 16)
    data.Start = mem.read_long(data.MapData + address.DtKs2)
    data.End = mem.read_long(data.MapData + address.DtJs2)
    data.ObjNum = (data.End - data.Start) / 24

    for data.obj_tmp in range(data.ObjNum):
        data.obj_ptr = mem.read_long(data.start + data.obj_tmp * 24)
        data.obj_ptr = mem.read_long(data.obj_ptr + 16) - 32
        if data.obj_ptr > 0:
            data.obj_type_a = mem.read_int(data.obj_ptr + address.LxPyAddr)
            data.obj_camp = mem.read_int(data.obj_ptr + address.ZyPyAddr)
            data.obj_code = mem.read_int(data.obj_ptr + address.DmPyAddr)
            if data.obj_type_a == 529 or data.obj_type_a == 545 or data.obj_type_a == 273 or data.obj_type_a == 61440:
                data.obj_blood = mem.read_long(data.obj_ptr + address.GwXlAddr)
                if data.obj_camp > 0 and data.obj_code > 0 and data.obj_blood > 0 and data.obj_ptr != data.rw_addr:
                    monster_coordinate = map_obj.read_coordinate(data.obj_ptr)
                    call.skill_call(data.rw_addr, 54141, 99999, monster_coordinate.x, monster_coordinate.y, 0, 1.0)
