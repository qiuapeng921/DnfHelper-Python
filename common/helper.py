import psutil


def get_process_id_by_name(name: str) -> int:
    pid = 0
    ps = psutil.process_iter()
    for p in ps:
        if p.name() == name:
            pid = p.pid
            break

    return pid
