import ctypes
import os
import time
from configparser import ConfigParser


def path_exists(path):
    return os.path.exists(path)


def write_ini(filename, section, key, value):
    exists = os.path.exists(filename)
    cfg = ConfigParser()

    if exists:
        cfg.read(filename, encoding="utf-8-sig")

    if not cfg.has_section(section) and not cfg.has_option(section, key):
        cfg.add_section(section)

    cfg.set(section, key, str(value))

    with open(filename, 'w') as configfile:
        cfg.write(configfile)


def read_ini(filename, section, key) -> str:
    cfg = ConfigParser()
    cfg.read(filename, encoding="utf-8-sig")

    if cfg.has_section(section) and cfg.has_option(section, key):
        return cfg.get(section, key)

    return ""


def force_delete_file(file_path: str):
    """
    强制删除文件
    :param file_path: 文件路径
    :return:
    """
    kernel32 = ctypes.windll.kernel32

    # 使用unicode字符串
    CreateDirectory = kernel32.CreateDirectoryW
    MoveFile = kernel32.MoveFileW
    DeleteFile = kernel32.DeleteFileW
    RemoveDirectory = kernel32.RemoveDirectoryW

    class SECURITY_ATTRIBUTES(ctypes.Structure):
        _fields_ = [
            ("Length", ctypes.c_ulong),
            ("SecurityDescriptor", ctypes.c_void_p),
            ("InheritHandle", ctypes.c_ulong),
        ]

    temp_dir = os.path.join(os.environ["TEMP"], str(int(time.time())))
    temp_dir_wchar = ctypes.c_wchar_p(temp_dir)

    sa = SECURITY_ATTRIBUTES()
    sa.Length = ctypes.sizeof(SECURITY_ATTRIBUTES)
    sa.SecurityDescriptor = None
    sa.InheritHandle = 0

    res1 = CreateDirectory(temp_dir_wchar, ctypes.pointer(sa))
    res2 = CreateDirectory(ctypes.c_wchar_p(temp_dir + "\\....\\"), ctypes.pointer(sa))
    res3 = MoveFile(ctypes.c_wchar_p(file_path), ctypes.c_wchar_p(temp_dir + "\\....\\TemporaryFile"))
    res4 = MoveFile(ctypes.c_wchar_p(temp_dir + "\\....\\"), ctypes.c_wchar_p(temp_dir + "\\TemporaryFile"))
    res5 = DeleteFile(ctypes.c_wchar_p(temp_dir + "\\TemporaryFile\\TemporaryFile"))
    res6 = RemoveDirectory(ctypes.c_wchar_p(temp_dir + "\\TemporaryFile"))
    res7 = RemoveDirectory(temp_dir_wchar)

    print(res1, res2, res3, res4, res5, res6, res7)


def main():
    # file_path = "C:\\TPqd640.sys"  # 更改为实际的文件路径
    # force_delete_file(file_path)
    # print("文件已成功删除")

    cfg_name = "C:\\666.ini"
    conf_exists = path_exists(cfg_name)
    if not conf_exists:
        write_ini(cfg_name, "default", "count", "1")

    complete_number = read_ini(cfg_name, "default", "count")
    print(complete_number)


if __name__ == "__main__":
    main()
