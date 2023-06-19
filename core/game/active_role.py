def active_role_map(level):
    if level <= 1:
        return 9501  # 流动的丛林
    elif level <= 5:
        return 9507  # 前往格拉卡
    elif level <= 10:
        return 9502  # 净化大魔法阵
    elif 15 <= level <= 19:
        return 9503  # 探查天空之城
    elif 20 <= level <= 24:
        return 9504  # 浮空之城
    elif 25 <= level <= 27:
        return 9511  # 解救马塞尔
    elif 28 <= level <= 29:
        return 9512  # 使徒罗特斯
    elif 30 <= level <= 33:
        return 9513  # 蜘蛛王国
    elif 34 <= level <= 37:
        return 9514  # 暗黑城入口
    elif 38 <= level <= 39:
        return 9533  # 令人恐惧的传染病
    elif 40 <= level <= 42:
        return 9534  # 疾病的根源
    elif 43 <= level <= 45:
        return 9561  # 悲剧在现
    elif 46 <= level <= 48:
        return 9562  # 吹笛子的男人
    elif 49 <= level <= 50:
        return 9563  # 使徒与搜捕团
    elif 51 <= level <= 53:
        return 9531  # 苏醒的斯卡萨
    elif 54 <= level <= 55:
        return 9532  # 雪山的主人
    elif 56 <= level <= 57:
        return 9572  # 根特防御战
    elif 58 <= level <= 61:
        return 9573  # 皇都军的逆袭
    elif 62 <= level <= 63:
        return 9574  # 卡勒特歼灭战
    elif level == 64:
        return 9524  # 夺回海上列车
    elif level == 65:
        return 9525  # 阿登高地
    elif 66 <= level <= 68:
        return 9526  # 战争结束
    elif 69 <= level <= 70:
        return 9551  # 向混乱的时空进发
    elif 71 <= level <= 72:
        return 9552  # 超越级别的魔法师
    elif level == 73:
        return 9553  # 身份暴露
    elif level == 74:
        return 9554  # 艾丽丝之谜
    elif level == 75:
        return 9555  # 能源被夺
    elif 76 <= level <= 77:
        return 9556  # 收复能源中心
    elif level == 78:
        return 9505  # 逃亡的安图恩
    elif level == 79:
        return 9591  # 凝聚光的地方
    elif level == 80:
        return 9592  # 寂静城防御系统
    elif level == 81:
        return 9594  # 传说之城秘密区域
    elif level == 82:
        return 9557  # 送光者
    elif level == 83:
        return 9515  # 充满嘶喊的地方
    elif level == 84:
        return 9517  # 中央公园森林
    elif level == 85:
        return 9535  # 亡命杀阵的恶魔
    elif level == 86:
        return 9537  # 燃烧的黑暗都市
    elif level == 87:
        return 9539  # 皇家娱乐的秘密
    elif 88 <= level <= 91:
        return 9541  # 金色星球
    elif 92 <= level <= 93:
        return 100003016  # 被夺走的皇宫
    elif level == 94:
        return 100003017  # 花园亭小路
    elif 95 <= level <= 96:
        return 100003018  # 记忆之地
    elif 97 <= level <= 98:
        return 100003019  # 暗黑神殿
    elif level == 99:
        return 100003275  # 真正的觉醒
    elif level == 100:
        return 100003421  # 黑暗教团的入侵
    elif level == 101:
        return 100003422  # 通向混沌王座之路
    elif level == 102:
        return 100003423  # 雷米迪奥斯的圣域
    elif level == 103:
        return 100003424  # 讨伐诺斯匹斯
    elif level == 104:
        return 100003425  # 异次元的预言所
    elif 105 <= level <= 106:
        return 100003426  # 阻截盖波加
    elif level == 107:
        return 100003427  # 机械崛起
    elif level == 108:
        return 100003428  # 熄灭龙焰
    elif level == 109:
        return 100003429  # 记忆之书
    return 0
