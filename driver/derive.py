import win32service as service
import winerror as error


class MemoryRw:
    # SCM句柄
    _hSCManager = int
    # 服务句柄
    _hService = None

    def __init__(self):
        pass

    def load_driver(self, driver_path: str, service_name: str, display_name: str) -> bool:
        """
        加载驱动
        :param driver_path 驱动路径
        :param service_name 驱动名称
        :param display_name 显示名称
        :return boolean
        """
        result = False

        self._hSCManager = service.OpenSCManager(None, None, service.SC_MANAGER_ALL_ACCESS)
        if self._hSCManager == 0:
            return False

        try:
            self._hService = service.CreateService(self._hSCManager, service_name, display_name,
                                                   service.SERVICE_ALL_ACCESS, service.SERVICE_KERNEL_DRIVER,
                                                   service.SERVICE_DEMAND_START, service.SERVICE_ERROR_IGNORE,
                                                   driver_path, None, 0, None, None, None)
        except service.error as create_err:
            # 1073 服务已经存在
            if create_err.winerror == error.ERROR_SERVICE_EXISTS:
                self._hService = service.OpenService(self._hSCManager, service_name, service.SC_MANAGER_ALL_ACCESS)

            try:
                start_service_res = service.StartService(self._hService, None)
                if start_service_res is None:
                    result = True
            except service.error as start_err:
                # 1056 服务运行,1072服务标记删除
                if start_err.winerror in [error.ERROR_SERVICE_ALREADY_RUNNING, error.ERROR_SERVICE_MARKED_FOR_DELETE]:
                    result = True
                else:
                    service.CloseServiceHandle(self._hService)
        if int(self._hService) <= 0:
            service.CloseServiceHandle(self._hSCManager)

        return result

    def un_load_driver(self) -> tuple:
        """驱动卸载"""
        try:
            status = service.ControlService(self._hService, service.SERVICE_CONTROL_STOP)
        finally:
            service.CloseServiceHandle(self._hService)

        service.CloseServiceHandle(self._hSCManager)

        return status
