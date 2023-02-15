import win32service
import winerror


class MemoryRw:
    # SCM句柄
    _hSCManager = int
    # 服务句柄
    _hService = None

    def __init__(self):
        pass

    def load_driver(self, driver_path: str, service_name: str, display_name: str) -> bool:
        result = bool

        self._hSCManager = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
        if self._hSCManager == 0:
            return False

        try:
            self._hService = win32service.CreateService(self._hSCManager, service_name, display_name,
                                                        win32service.SERVICE_ALL_ACCESS,
                                                        win32service.SERVICE_KERNEL_DRIVER,
                                                        win32service.SERVICE_DEMAND_START,
                                                        win32service.SERVICE_ERROR_IGNORE,
                                                        driver_path, None, 0, None, None, None)
        except win32service.error as create_err:
            # 1073 服务已经存在
            if create_err.winerror == winerror.ERROR_SERVICE_EXISTS:
                self._hService = win32service.OpenService(self._hSCManager, service_name,
                                                          win32service.SC_MANAGER_ALL_ACCESS)
            try:
                win32service.StartService(self._hService, None)
            except win32service.error as start_err:
                # 1056 服务运行,1072服务标记删除
                if start_err.winerror == winerror.ERROR_SERVICE_ALREADY_RUNNING or start_err.winerror == winerror.ERROR_SERVICE_MARKED_FOR_DELETE:
                    result = True
            finally:
                win32service.CloseServiceHandle(self._hService)
        finally:
            win32service.CloseServiceHandle(self._hSCManager)

        return result

    def un_load_driver(self, service_name: str):
        try:
            self._hService = win32service.OpenService(self._hSCManager, service_name, win32service.SERVICE_ALL_ACCESS)
            try:
                status = win32service.ControlService(self._hService, win32service.SERVICE_CONTROL_STOP)
            finally:
                win32service.CloseServiceHandle(self._hService)
        except win32service.error as start_err:
            print(start_err.winerror)
        finally:
            win32service.CloseServiceHandle(self._hSCManager)

        return status
