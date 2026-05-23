#定义函数

#def 函数名(参数列表):
#    函数体
#    return 返回值

def add(x,y):
    return x+y 

result = add(1,2)
print(result)


#位置参数和关键字参数

# def make_judgement(a, b, c):
#     """判断三条边的长度能否构成三角形"""
#     return a + b > c and b + c > a and a + c > b

# print(make_judgement(3, 4, 5)) # True
# print(make_judgement(1, 2, 3)) # False
# print(make_judgement(b=2, c=3, a=1))  # False
# print(make_judgement(c=6, b=4, a=5))  # True

#强制位置参数
def make_judgement_1(a, b, c, /):    #/前面的参数是强制位置参数
    """判断三条边的长度能否构成三角形"""
    return a + b > c and b + c > a and a + c > b
print(make_judgement_1(3, 4, 5))#所谓强制位置参数，就是调用函数时只能按照参数位置来接收参数值的参数
# print(make_judgement_1(a=2, b=3, c=1))

#强制关键字参数
def make_judgement_2(*, a, b, c):   # *后面的参数是命名关键字参数
    """判断三条边的长度能否构成三角形"""
    return a + b > c and b + c > a and a + c > b
print(make_judgement_2(a=2, b=3, c=1))
#print(make_judgement_2(3, 4, 5))#所谓强制关键字参数，就是调用函数时只能按照参数名来接收参数值的参数


#参数的默认值
def greet(name, greeting="Hello"): #greeting参数有默认值"Hello"，如果调用函数时没有提供greeting参数的值，就会使用默认值
    return f"{greeting}, {name}!"

print(greet("Alice"))  # 输出: Hello, Alice!
print(greet("Bob", "Hi"))  # 输出: Hi, Bob!
#注意：默认参数必须放在非默认参数的后面，否则会导致语法错误
# def greet(greeting="Hello", name):  # 语法错误，默认参数


#可变参数

#***************元组********************#
# 用星号表达式来表示args可以接收0个或任意多个参数
# 调用函数时传入的n个参数会组装成一个n元组赋给args
# 如果一个参数都没有传入，那么args会是一个空元组
def add(*args):
    total = 0
    # 对保存可变参数的元组进行循环遍历
    for val in args:
        # 对参数进行了类型检查（数值型的才能求和）
        if type(val) in (int, float):
            total += val
    return total

# 在调用add函数时可以传入0个或任意多个参数
print(add())         # 0
print(add(1))        # 1
print(add(1, 2, 3))  # 6
print(add(1, 2, 'hello', 3.45, 6))  # 12.45

#***************字典********************#
# 参数列表中的**kwargs可以接收0个或任意多个关键字参数
# 调用函数时传入的关键字参数会组装成一个字典（参数名是字典中的键，参数值是字典中的值）
# 如果一个关键字参数都没有传入，那么kwargs会是一个空字典
def foo(*args, **kwargs):
    print(args)
    print(kwargs)


foo(3, 2.1, True, name='骆昊', age=43, gpa=4.95)


#用模块管理函数
#例子1
# import module1
# import module2

# # 用“模块名.函数名”的方式（完全限定名）调用函数，
# module1.foo()  # hello, world!
# module2.foo()  # goodbye, world!
#例子2
# import module1 as m1
# import module2 as m2

# m1.foo()  # hello, world!
# m2.foo()  # goodbye, world!
#例子3
# from module1 import foo as f1
# from module2 import foo as f2

# f1()  # hello, world!
# f2()  # goodbye, world!


#标准库中的模块和函数
import math, random, time   #导入math、random和time模块，math模块提供了数学相关的函数和常量，random模块提供了生成随机数的函数，time模块提供了处理时间相关的函数。
#内置函数是Python内置的函数，可以直接使用，无需导入任何模块。以下是一些常用的内置函数：
# abs	返回一个数的绝对值，例如：abs(-1.3)会返回1.3。
# bin	把一个整数转换成以'0b'开头的二进制字符串，例如：bin(123)会返回'0b1111011'。
# chr	将Unicode编码转换成对应的字符，例如：chr(8364)会返回'€'。
# hex	将一个整数转换成以'0x'开头的十六进制字符串，例如：hex(123)会返回'0x7b'。
# input	从输入中读取一行，返回读到的字符串。
# len	获取字符串、列表等的长度。
# max	返回多个参数或一个可迭代对象中的最大值，例如：max(12, 95, 37)会返回95。
# min	返回多个参数或一个可迭代对象中的最小值，例如：min(12, 95, 37)会返回12。
# oct	把一个整数转换成以'0o'开头的八进制字符串，例如：oct(123)会返回'0o173'。
# open	打开一个文件并返回文件对象。
# ord	将字符转换成对应的Unicode编码，例如：ord('€')会返回8364。
# pow	求幂运算，例如：pow(2, 3)会返回8；pow(2, 0.5)会返回1.4142135623730951。
# print	打印输出。
# range	构造一个范围序列，例如：range(100)会产生0到99的整数序列。
# round	按照指定的精度对数值进行四舍五入，例如：round(1.23456, 4)会返回1.2346。
# sum	对一个序列中的项从左到右进行求和运算，例如：sum(range(1, 101))会返回5050。
# type	返回对象的类型，例如：type(10)会返回int；而 type('hello')会返回str。

