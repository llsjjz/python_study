#高阶函数

def calc(init_value, op_func, *args, **kwargs):#op_func是一个函数，*args是一个元组，**kwargs是一个字典
    items = list(args) + list(kwargs.values())
    result = init_value
    for item in items:
        if type(item) in (int, float):
            result = op_func(result, item)
    return result

def add(x, y):
    return x + y

def mul(x, y):
    return x * y

print(calc(0, add, 1, 2, 3, a=4, b=5))
print(calc(1, mul, 2, 3, a=4, b=5))

    #map和filter函数
def is_even(num):
    """判断num是不是偶数"""
    return num % 2 == 0

def square(num):
    """求平方"""
    return num ** 2

old_nums = [35, 12, 8, 99, 60, 52]
new_nums = list(map(square, filter(is_even, old_nums)))#map功能是对可迭代对象的每个元素执行一个函数，filter功能是过滤掉不满足条件的元素
print(new_nums)  # [144, 64, 3600, 2704]

    #sorted函数->区别sorted函数可以对可迭代对象进行排序，返回一个新的列表，而sort方法是列表对象的方法，会直接修改原列表。
old_strings = ['in', 'apple', 'zoo', 'waxberry', 'pear']
new_strings = sorted(old_strings, key=len)
print(new_strings)  # ['in', 'zoo', 'pear', 'apple', 'waxberry']


#lambda表达式->匿名函数
"""
定义 lambda 函数的关键字是lambda
后面跟函数的参数，如果有多个参数用逗号进行分隔；
冒号后面的部分就是函数的执行体，通常是一个表达式，
表达式的运算结果就是 lambda 函数的返回值，不需要写return 关键字。
"""
old_nums = [35, 12, 8, 99, 60, 52]
new_nums = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, old_nums)))#lambda x: x ** 2是一个匿名函数，lambda x: x % 2 == 0也是一个匿名函数
print(new_nums)  # [144, 64, 3600, 2704]

import functools
import operator

# 用一行代码实现计算阶乘的函数
fac = lambda n: functools.reduce(operator.mul, range(2, n + 1), 1)#functools.reduce函数会对参数序列中元素进行累积，operator.mul功能是对两个参数进行乘法运算，range(2, n + 1)是一个可迭代对象，表示从2到n的整数，1是reduce函数的初始值，如果不指定初始值，则默认使用序列中的第一个元素作为初始值。

# 用一行代码实现判断素数的函数
is_prime = lambda x: all(map(lambda f: x % f, range(2, int(x ** 0.5) + 1)))#all函数会对可迭代对象中的元素进行判断，如果所有元素都为True，则返回True，否则返回False。map函数会对可迭代对象中的每个元素执行一个函数，lambda f: x % f是一个匿名函数，range(2, int(x ** 0.5) + 1)是一个可迭代对象，表示从2到x的平方根的整数部分加1的范围内的所有整数。

# 调用Lambda函数
print(fac(6))        # 720
print(is_prime(37))  # True


#偏函数
import functools

int2 = functools.partial(int, base=2)#functools.partial函数会返回一个新的函数，这个新函数的参数已经被固定了，base=2表示这个新函数的参数base已经被固定为2了，所以这个新函数就相当于int函数的一个特例了，也就是说这个新函数就是一个将字符串转换为二进制整数的函数了。同样的，int8就是一个将字符串转换为八进制整数的函数，int16就是一个将字符串转换为十六进制整数的函数了。
int8 = functools.partial(int, base=8)
int16 = functools.partial(int, base=16)

print(int('1001'))    # 1001

print(int2('1001'))   # 9
print(int8('1001'))   # 513
print(int16('1001'))  # 4097

