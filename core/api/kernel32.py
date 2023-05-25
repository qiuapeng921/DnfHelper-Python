import win32api
import win32process


def open_process(pid: int) -> int:
    handle = win32api.OpenProcess(2097151, False, pid)

    return handle


def close_process(handle: int) -> int:
    return win32api.CloseHandle(handle)


def write_byte_arr(addr: int, data: bytes) -> bool:
    handle = open_process(1)
    win32process.WriteProcessMemory(handle, addr, data, len(data))
    return True


def read_byte_arr(addr: int, data: bytes) -> bool:
    handle = open_process(1)
    try:
        win32process.ReadProcessMemory(handle, addr, data, len(data))
    except Exception as msg:
        print(msg)
    finally:
        close_process(handle)
    return True
