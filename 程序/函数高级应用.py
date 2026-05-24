#装饰器(难点)
'''
装饰器是“用一个函数装饰另外一个函数并为其提供额外的能力”的语法现象
'''
import random
import time
from functools import wraps

def download(filename):
    """下载文件"""
    print(f'开始下载{filename}.')
    time.sleep(random.random() * 6)
    print(f'{filename}下载完成.')
 
def upload(filename):
    """上传文件"""
    print(f'开始上传{filename}.')
    time.sleep(random.random() * 8)
    print(f'{filename}上传完成.')

#打印花费时间
# start = time.time()
# download('MySQL从删库到跑路.avi')
# end = time.time()
# print(f'花费时间: {end - start:.2f}秒')
# start = time.time()
# upload('Python从入门到住院.pdf')
# end = time.time()
# print(f'花费时间: {end - start:.2f}秒')

    #装饰器
def record_time(func):

    @wraps(func)#还原被装饰函数的元信息
    def wrapper(*args, **kwargs):
        # 在执行被装饰的函数之前记录开始时间
        start = time.time()
        # 执行被装饰的函数并获取返回值
        result = func(*args, **kwargs)
        # 在执行被装饰的函数之后记录结束时间
        end = time.time()
        # 计算和显示被装饰函数的执行时间
        print(f'{func.__name__}执行时间: {end - start:.2f}秒')
        # 返回被装饰函数的返回值
        return result
    
    return wrapper
    #装饰器使用
# download = record_time(download)
# upload = record_time(upload)
# download('MySQL从删库到跑路.avi')
# upload('Python从入门到住院.pdf')

        #语法糖
@record_time
def download(filename):
    print(f'开始下载{filename}.')
    time.sleep(random.random() * 6)
    print(f'{filename}下载完成.')

@record_time
def upload(filename):
    print(f'开始上传{filename}.')
    time.sleep(random.random() * 8)
    print(f'{filename}上传完成.')
        #语法糖使用装饰器
# download('MySQL从删库到跑路.avi')
# upload('Python从入门到住院.pdf')

        #还原语法糖
# # 调用装饰后的函数会记录执行时间
# download('MySQL从删库到跑路.avi')
# upload('Python从入门到住院.pdf')
# # 取消装饰器的作用不记录执行时间
# download.__wrapped__('MySQL必知必会.pdf')
# upload.__wrapped__('Python从新手到大师.pdf')


#递归调用
def factorial(n):
    """计算n的阶乘"""
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)#递归调用函数本身，直到达到基准情况（n == 0）时返回结果。
    
print(factorial(5))  # 120



from functools import lru_cache

@lru_cache()#lru_cache装饰器会缓存函数的返回值，当函数被调用时，如果参数已经存在于缓存中，则直接返回缓存中的结果，而不需要重新计算。这可以显著提高递归函数的性能，特别是对于斐波那契数列等具有重叠子问题的函数。
def fib1(n):
    if n in (1, 2):
        return 1
    return fib1(n - 1) + fib1(n - 2)


for i in range(1, 51):
    print(i, fib1(i))