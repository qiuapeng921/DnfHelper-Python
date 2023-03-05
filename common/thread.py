import ctypes
import inspect
import threading
import time


class MyThreadFunc(object):
    """手动终止线程的方法"""
    def __init__(self, func, args_tup):
        self.myThread = threading.Thread(target=func, args=args_tup)

    def start(self):
        print('线程启动')
        self.myThread.start()

    def stop(self):
        print('线程终止')
        try:
            for i in range(5):
                self.async_raise(self.myThread.ident, SystemExit)
                time.sleep(1)
        except Exception as e:
            print(e)

    def async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")


if __name__ == '__main__':
    # 定义一个读秒器
    def second_count(arg1, arg2):
        i = 0
        while True:
            i += 1
            print("{}-{}: {}".format(arg1, arg2, i))
            time.sleep(1)

    # 声明一个线程类
    mythread = MyThreadFunc(second_count, ("好耶", "haoye"))

    # 启动 --------------------------------------
    mythread.start()

    # 等待三秒
    time.sleep(3)

    # 查看线程状态
    mythread.state()

    # 等待三秒
    time.sleep(3)

    # 终止线程 ----------------------------------
    mythread.stop()

    # 等待三秒
    time.sleep(3)

    # 再次查看线程状态
    mythread.state()