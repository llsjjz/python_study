#例子1：随机验证码
#设计一个生成随机验证码的函数，验证码由数字和英文大小写字母构成，长度可以通过参数设置。

import random
import string

ALL_CHARS = string.digits + string.ascii_letters#string.digits包含了所有的数字字符（0-9），string.ascii_letters包含了所有的英文字母字符（包括大写和小写）。通过将这两个字符串连接起来，我们得到了一个包含所有数字和英文字母的字符串ALL_CHARS。

def generate_code(*, code_len=4):
    """
    生成指定长度的验证码
    :param code_len: 验证码的长度(默认4个字符)
    :return: 由大小写英文字母和数字构成的随机验证码字符串
    """
    return ''.join(random.choices(ALL_CHARS, k=code_len))#random.choices()函数从ALL_CHARS字符串中随机选择code_len个字符，并返回一个列表。然后，使用''.join()方法将这个列表中的字符连接成一个字符串，最终得到生成的验证码。

print(generate_code())  # 4个字符的验证码

# 例子2：判断素数
# 设计一个判断给定的大于1的正整数是不是质数的函数。
def is_prime(num: int) -> bool:
    """
    判断一个正整数是不是质数
    :param num: 大于1的正整数
    :return: 如果num是质数返回True，否则返回False
    """
    for i in range(2, int(num ** 0.5) + 1):#对于一个大于1的正整数num，如果它不是质数，那么它一定有一个小于或等于sqrt(num)的因子。因此，我们只需要检查从2到sqrt(num)之间的整数是否能整除num。如果存在这样的整数i，使得num % i == 0，那么num就不是质数，函数返回False。如果循环结束后没有找到任何能整除num的整数，那么num就是质数，函数返回True。
        if num % i == 0:
            return False
    return True
print(is_prime(7))   # True
print(is_prime(10))  # False

#例子3：最大公约数和最小公倍数
def lcm(x: int, y: int) -> int:
    """求最小公倍数"""
    return x * y // gcd(x, y)


def gcd(x: int, y: int) -> int:
    """求最大公约数"""
    while y % x != 0:
        x, y = y % x, x
    return x

print(gcd(12, 15))  # 输出: 3
print(lcm(12, 15))  # 输出: 60

#例子4：数据统计
def ptp(data):
    """极差（全距）"""
    return max(data) - min(data)


def mean(data):
    """算术平均"""
    return sum(data) / len(data)


def median(data):
    """中位数"""
    temp, size = sorted(data), len(data)
    if size % 2 != 0:
        return temp[size // 2]
    else:
        return mean(temp[size // 2 - 1:size // 2 + 1])


def var(data, ddof=1):
    """方差"""
    x_bar = mean(data)
    temp = [(num - x_bar) ** 2 for num in data]
    return sum(temp) / (len(temp) - ddof)


def std(data, ddof=1):
    """标准差"""
    return var(data, ddof) ** 0.5


def cv(data, ddof=1):
    """变异系数"""
    return std(data, ddof) / mean(data)


def describe(data):
    """输出描述性统计信息"""
    print(f'均值: {mean(data)}')
    print(f'中位数: {median(data)}')
    print(f'极差: {ptp(data)}')
    print(f'方差: {var(data)}')
    print(f'标准差: {std(data)}')
    print(f'变异系数: {cv(data)}')

data = [10, 12, 23, 23, 16, 23, 21, 16]
describe(data)

#例子5：双色球随机选号
"""
双色球随机选号程序

Author: 骆昊
Version: 1.3
"""
import random

RED_BALLS = [i for i in range(1, 34)]
BLUE_BALLS = [i for i in range(1, 17)]


def choose():
    """
    生成一组随机号码
    :return: 保存随机号码的列表
    """
    selected_balls = random.sample(RED_BALLS, 6)
    selected_balls.sort()
    selected_balls.append(random.choice(BLUE_BALLS))
    return selected_balls


def display(balls):
    """
    格式输出一组号码
    :param balls: 保存随机号码的列表
    """
    for ball in balls[:-1]:
        print(f'\033[031m{ball:0>2d}\033[0m', end=' ')
    print(f'\033[034m{balls[-1]:0>2d}\033[0m')


n = int(input('生成几注号码: '))
for _ in range(n):
    display(choose())

