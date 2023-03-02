import psutil


def get_process_id_by_name(name: str) -> int:
    pid = 0
    ps = psutil.process_iter()
    for p in ps:
        if p.name() == name:
            pid = p.pid
            break

    return pid


hr_t, min_t, sec_t = (0, 0, 0)


def get_app_run_time():
    """获取app运行时间"""
    global hr_t, min_t, sec_t
    sec_t = sec_t + 1
    if sec_t == 60:
        sec_t = 0
        min_t = min_t + 1
    if min_t == 60:
        min_t = 0
        hr_t = hr_t + 1
    string = "{}:{}:{}".format(hr_t, min_t, sec_t)
    return string
