from common import convert
from game import call, address


class Pack:
    data = []

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def hc_call(cls, params):
        """
        缓冲call
        :param params:
        :return:
        """
        cls.data = call.sub_rsp(256)
        cls.data = convert.add_list(cls.data, [72, 185], convert.int_to_bytes(address.FbAddr, 8))
        cls.data = convert.add_list(cls.data, [186], convert.int_to_bytes(params, 4))
        cls.data = convert.add_list(cls.data, [72, 184], convert.int_to_bytes(address.HcCallAddr, 8))
        cls.data = convert.add_list(cls.data, [255, 208])
        cls.data = convert.add_list(cls.data, call.add_rsp(256))

    def jm_call(cls, params, len):
        """加密call
        :param params: int
        :param len: int
        :return:
        """
        cls.data = convert.add_list(cls.data, call.sub_rsp(256))
        cls.data = convert.add_list(cls.data, [72, 185], convert.int_to_bytes(address.FbAddr, 8))
        cls.data = convert.add_list(cls.data, [72, 186], convert.int_to_bytes(params, 8))
        if len == 1:
            cls.data = convert.add_list(cls.data, [72, 184], convert.int_to_bytes(address.JmB1CallAddr, 8))
        if len == 2:
            cls.data = convert.add_list(cls.data, [72, 184], convert.int_to_bytes(address.JmB2CallAddr, 8))
        if len == 4:
            cls.data = convert.add_list(cls.data, [72, 184], convert.int_to_bytes(address.JmB3CallAddr, 8))
        if len == 8:
            cls.data = convert.add_list(cls.data, [72, 184], convert.int_to_bytes(address.JmB4CallAddr, 8))
        cls.data = convert.add_list(cls.data, [255, 208])
        cls.data = convert.add_list(cls.data, call.add_rsp(256))

    @classmethod
    def fb_call(cls):
        """
        发包call
        :return:
        """
        cls.data = convert.add_list(cls.data, call.sub_rsp(256))
        cls.data = convert.add_list(cls.data, [72, 184], convert.int_to_bytes(address.FbCallAddr, 8))
        cls.data = convert.add_list(cls.data, [255, 208])
        cls.data = convert.add_list(cls.data, call.add_rsp(256))
        call.compile_call(bytes(cls.data))
        cls.data.clear()
