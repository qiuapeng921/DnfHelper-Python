import numpy as np

chinese_str = '格兰迪发电站'
byte_str = chinese_str.encode('utf-8')
arr = np.frombuffer(byte_str, dtype=np.uint8)

print(arr)

# [60 104 112 81 234 143 209 83 53 117 217 122]


lst = [60, 104, 112, 81, 234, 143, 209, 83, 53, 117, 217, 122]
str_lst = [chr(i) for i in lst]
str_name = ''.join(str_lst)
print(str_name)



