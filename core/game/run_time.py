import hashlib
import random
import time

from common import logger

# 记录程序开始运行的时间
start_time = int(round(time.time()))


# 通关次数做取余
def modulo_algorithm(value, size):
    if value <= 0:
        return 0
    remainder = value % size  # 取余操作

    if remainder == 0:
        random_num = generate_random_number()  # 调用随机数算法
        sleep_time = random_num / 1000.0  # 将随机数转换为秒数
        logger.info("通关第{}次，睡眠{}秒".format(value, sleep_time), 1)
        time.sleep(sleep_time)  # 睡眠随机数返回的时间

    return remainder


def generate_random_number():
    current_time = int(round(time.time()))  # 获取当前时间戳
    elapsed_time = current_time - start_time  # 计算程序运行的时间差

    if elapsed_time < 2 * 60 * 60:  # 前2小时
        min_interval = 10 * 1000  # 最小区间为10毫秒
        max_interval = 1 * 60 * 1000  # 最大区间为1分钟
    elif elapsed_time < 3 * 60 * 60:  # 2小时-3小时
        min_interval = 1 * 60 * 1000  # 最小区间为1分钟
        max_interval = 5 * 60 * 1000  # 最大区间为5分钟
    elif elapsed_time < 4 * 60 * 60:  # 3小时-4小时
        min_interval = 5 * 60 * 1000  # 最小区间为5分钟
        max_interval = 10 * 60 * 1000  # 最大区间为10分钟
    else:  # 4小时之后
        min_interval = 10 * 60 * 1000  # 最小区间为10分钟
        max_interval = 20 * 60 * 1000  # 最大区间为20分钟

    interval = max_interval - min_interval  # 区间范围
    hash_value = hashlib.md5(str(current_time).encode()).hexdigest()  # 使用MD5散列算法生成哈希值
    scaled_hash = int(hash_value, 16) % interval  # 将哈希值转换为0到interval-1之间的数
    random_number = scaled_hash + min_interval  # 将数值范围平移到min_interval到max_interval之间
    return random_number


if __name__ == '__main__':
    # 测试生成随机数的算法
    for _ in range(10):
        dividend = random.randint(1, 1000)  # 生成一个1到1000之间的随机数
        result = modulo_algorithm(dividend, 15)
        print(result)