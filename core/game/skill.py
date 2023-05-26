import random
import time
import random

# 重新构建strings和weights
# 后续可以读技能名称处理
strings = ['z', 'x', 'c', 'v', 'a', 's', 'd', 'f', 'g', 'h', 'q', 'w', 'e', 'r', 't', 'y']
weights = [5, 5, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


def pick_strings(keys, num_picks, weights):
    if len(keys) != len(weights):
        raise ValueError("Length of strings and weights must be the same")
    if num_picks > len(keys):
        raise ValueError("Number of picks cannot be greater than the length of strings")

    # Calculate the cumulative sum of weights
    cum_weights = [0] * len(weights)
    cum_weights[0] = weights[0]
    for i in range(1, len(weights)):
        cum_weights[i] = cum_weights[i - 1] + weights[i]

    # Generate a list of random numbers between 0 and the total weight
    total_weight = cum_weights[-1]
    rand_nums = [random.randint(0, total_weight - 1) for _ in range(num_picks)]

    # Pick the strings based on the random numbers
    picks = []
    for rand_num in rand_nums:
        for i in range(len(cum_weights)):
            if rand_num < cum_weights[i]:
                picks.append(keys[i])
                break

    return picks


def pick_key(num_picks: int = 5):
    return pick_strings(strings, num_picks, weights)


if __name__ == '__main__':
    # 使用pick_strings方法进行随机选择
    picks = pick_strings(strings, 5, weights)
    print(picks)

    while True:
        picks = pick_key(5)
        time.sleep(0.5)
        print(picks);
