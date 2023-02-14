import win32api
import win32process


def openProcess(pid: int) -> int:
    handle = win32api.OpenProcess(2097151, False, pid)

    return handle


def closeProcess(handle: int) -> int:
    return win32api.CloseHandle(handle)


def WriteByteArr(addr: int, data: bytes) -> bool:
    handle = openProcess(1)
    win32process.WriteProcessMemory(handle, addr, data, len(data))
    return True


def ReadByteArr(addr: int, data: bytes) -> bool:
    handle = openProcess(1)
    try:
        win32process.ReadProcessMemory(handle, addr, data, len(data))
    except Exception as msg:
        print(msg)
    finally:
        closeProcess(handle)
    return True
