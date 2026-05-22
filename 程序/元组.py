#元组的定义和运算

t1 = (1, 2, 3)
t2 = ('hello', 'world',123.5)
print(t1)
print(type(t1))
print(t2)

print(t1[0])
print(t1[-1])
print(t1[0:2])
print(t1 + t2)
print(t1 * 2)

print(t1 <= (2, 3, 4))

a = ()
b = (1,)
c = (1)
print(type(a))
print(type(b))
print(type(c))

#打包和解包操作
t3 = 1, 2, 3
print(t3)
a, b, c = t3
print(a, b, c)

t4 = (1, 2, 3, 4, 5)
a, b, *c = t4#a的值为1，b的值为2，c的值为[3, 4, 5]
print(a, b, c)

s1 = 'hello'
a, b, c, d, e = s1
print(a, b, c, d, e)
a,*b,c = s1#a的值为h，b的值为['e', 'l', 'l']，c的值为o
print(a, b, c)

#交换变量的值
a = 1
b = 2
c = 3
a, b, c = c, a, b#交换后a的值为3，b的值为1，c的值为2
print(a, b, c)

#元组和列表的比较
import timeit

print('%.3f 秒' % timeit.timeit('[1, 2, 3, 4, 5, 6, 7, 8, 9]', number=10000000))
print('%.3f 秒' % timeit.timeit('(1, 2, 3, 4, 5, 6, 7, 8, 9)', number=10000000))#元组的创建和访问比列表更快，因为元组是不可变的，而列表是可变的。

l1 = [1, 2, 3]
t5 = ('a', 'b', 'c')
print(list(t5))#将元组转换为列表
print(tuple(l1))#将列表转换为元组   