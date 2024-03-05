from common import helper
from game import call, address


class Pack:
    data = []

    @classmethod
    def __init__(cls):
        cls.data = []

    @classmethod
    def hc_call(cls, params):
        """
        缓冲call
        :param params:
        :return:
        """
        cls.data = call.sub_rsp(256)
        cls.data = helper.add_list(cls.data, [72, 185], helper.int_to_bytes(address.FbAddr, 8))
        cls.data = helper.add_list(cls.data, [186], helper.int_to_bytes(params, 4))
        cls.data = helper.add_list(cls.data, [72, 184], helper.int_to_bytes(address.HcCallAddr, 8))
        cls.data = helper.add_list(cls.data, [255, 208])
        cls.data = helper.add_list(cls.data, call.add_rsp(256))

    @classmethod
    def jm_call(cls, params, length):
        """加密call
        :param params: int
        :param length: int
        :return:
        """
        cls.data = helper.add_list(cls.data, call.sub_rsp(256))
        cls.data = helper.add_list(cls.data, [72, 185], helper.int_to_bytes(address.FbAddr, 8))
        cls.data = helper.add_list(cls.data, [72, 186], helper.int_to_bytes(params, 8))
        if length == 1:
            cls.data = helper.add_list(cls.data, [72, 184], helper.int_to_bytes(address.JmB1CallAddr, 8))
        if length == 2:
            cls.data = helper.add_list(cls.data, [72, 184], helper.int_to_bytes(address.JmB2CallAddr, 8))
        if length == 4:
            cls.data = helper.add_list(cls.data, [72, 184], helper.int_to_bytes(address.JmB3CallAddr, 8))
        if length == 8:
            cls.data = helper.add_list(cls.data, [72, 184], helper.int_to_bytes(address.JmB4CallAddr, 8))
        cls.data = helper.add_list(cls.data, [255, 208])
        cls.data = helper.add_list(cls.data, call.add_rsp(256))

    @classmethod
    def fb_call(cls):
        """
        发包call
        :return:
        """
        cls.data = helper.add_list(cls.data, call.sub_rsp(256))
        cls.data = helper.add_list(cls.data, [72, 184], helper.int_to_bytes(address.FbCallAddr, 8))
        cls.data = helper.add_list(cls.data, [255, 208])
        cls.data = helper.add_list(cls.data, call.add_rsp(256))
        call.compile_call(cls.data)
        cls.data.clear()

    @classmethod
    def return_role(cls):
        """组包返回角色"""
        cls.hc_call(7)
        cls.fb_call()

    @classmethod
    def select_role(cls, index):
        """组包选择角色"""
        if index == 0:
            return
        cls.hc_call(4)
        cls.jm_call(index, 2)
        cls.fb_call()

    @classmethod
    def select_map(cls):
        """组包选图"""
        cls.hc_call(15)
        cls.jm_call(0, 4)
        cls.fb_call()

    @classmethod
    def go_map(cls, bh, nd, sy, lx):
        """组包进图"""
        cls.hc_call(16)
        cls.jm_call(bh, 4)
        cls.jm_call(nd, 1)
        cls.jm_call(0, 2)
        cls.jm_call(sy, 1)
        cls.jm_call(lx, 1)
        cls.jm_call(65535, 2)
        cls.jm_call(0, 4)
        cls.jm_call(0, 1)
        cls.jm_call(0, 4)
        cls.jm_call(0, 1)
        cls.jm_call(0, 4)
        cls.fb_call()

    @classmethod
    def get_income(cls, h: int, l: int):
        """组包翻牌"""
        cls.hc_call(69)
        cls.fb_call()
        cls.hc_call(70)
        cls.fb_call()
        cls.hc_call(71)
        cls.jm_call(h, 1)
        cls.jm_call(l, 1)
        cls.fb_call()
        cls.hc_call(1426)
        cls.fb_call()

    @classmethod
    def leave_map(cls):
        """组包出图"""
        cls.hc_call(42)
        cls.fb_call()

    @classmethod
    def move_map(cls, max_map, mix_map, x, y):
        """组包移动"""
        if max_map < 0 or mix_map < 0 or x < 0 or y < 0:
            return
        cls.hc_call(36)
        cls.jm_call(max_map, 4)
        cls.jm_call(mix_map, 4)
        cls.jm_call(x, 2)
        cls.jm_call(y, 2)
        cls.jm_call(5, 1)
        cls.jm_call(78, 4)
        cls.jm_call(1, 2)
        cls.jm_call(0, 4)
        cls.jm_call(0, 1)
        cls.jm_call(0, 1)
        cls.fb_call()

    @classmethod
    def pick_up(cls, addr):
        """组包拾取"""
        if addr < 0:
            return
        cls.hc_call(43)
        cls.jm_call(addr, 4)
        cls.jm_call(0, 1)
        cls.jm_call(1, 1)
        cls.jm_call(420, 2)
        cls.jm_call(254, 2)
        cls.jm_call(4501, 2)
        cls.jm_call(435, 2)
        cls.jm_call(271, 2)
        cls.jm_call(22624, 2)
        cls.jm_call(28402, 2)
        cls.jm_call(0, 1)
        cls.fb_call()

    @classmethod
    def decomposition(cls, addr):
        """组包分解"""
        if addr < 0:
            return
        cls.hc_call(26)
        cls.jm_call(0, 1)
        cls.jm_call(65535, 2)
        cls.jm_call(317, 4)
        cls.jm_call(1, 1)
        cls.jm_call(addr, 2)
        cls.fb_call()

    @classmethod
    def tidy_backpack(cls, pack_type, pack_addr):
        """整理背包"""
        cls.hc_call(20)
        cls.jm_call(6, 4)
        cls.jm_call(16, 1)
        cls.jm_call(pack_type, 1)  # 1 装备 2消耗品 3材料 4任务 10副职业
        cls.jm_call(24, 1)
        cls.jm_call(pack_addr, 1)  # 0 背包 2个人仓库 12账号金库
        cls.jm_call(32, 1)
        cls.jm_call(0, 1)  # 0 栏位排序 1品级排序 2Lv排序 3部位排序
        cls.fb_call()

    @classmethod
    def accept_task(cls, task_id):
        """接受任务"""
        cls.hc_call(31)
        cls.jm_call(31, 2)
        cls.jm_call(task_id, 2)
        cls.fb_call()

    @classmethod
    def give_up_task(cls, task_id):
        """放弃任务"""
        cls.hc_call(32)
        cls.jm_call(32, 2)
        cls.jm_call(task_id, 2)
        cls.fb_call()

    @classmethod
    def finish_task(cls, task_id):
        """完成任务"""
        cls.hc_call(33)
        cls.jm_call(33, 2)
        cls.jm_call(task_id, 2)
        cls.jm_call(0, 1)
        cls.jm_call(0, 1)
        cls.fb_call()

    @classmethod
    def submit_task(cls, task_id):
        """提交任务"""
        cls.hc_call(34)
        cls.jm_call(34, 2)
        cls.jm_call(task_id, 2)
        cls.jm_call(65535, 2)
        cls.jm_call(1, 2)
        cls.jm_call(65535, 2)
        cls.fb_call()
