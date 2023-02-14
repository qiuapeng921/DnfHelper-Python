import win32api
import win32service


def derive():
    process_handle = win32api.OpenProcess(2097151, False, 9128)
    manager_handle = win32service.OpenSCManager(None, None, 0xf003f)
    print(process_handle, manager_handle)
