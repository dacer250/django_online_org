import random
import time
from collections import namedtuple

start_time = time.time()
shuangseqiu = namedtuple('shuangseqiu', ['red', 'blue'])
my_nums = shuangseqiu(red=[8,12,19,21,22,25], blue=[13])
total = 0
times = 100000000


def my_range(my_time):
    for i in range(my_time):
        yield i


for i in my_range(my_time=times):
# for i in range(times):
    red = sorted(random.sample(range(1, 34), 6))
    blue = random.sample(range(1, 17), 1)
    result = shuangseqiu(red, blue)
    if my_nums == result:
         total += 1
end_time = time.time()
total_time = end_time - start_time
print(total, total_time)
