#创建列表
"""
a = [1, 2, 3, 4, 5]
b = ['a', 'b', 'c', 'd', 'e']
c = [1, 'a', 2.5, True]
d = list(range(1, 6))
e = list('hello')
print(a)
print(b)
print(c)
print(d)
print(e)

"""

#列表运算

"""

#列表的加法和乘法
a = [1, 2, 3]
b = [4, 5, 6]
c = ['a', 'b', 'c']
print(a+b)
print(a+c)
print(a*3)
print(c*2)

#in和not in
print( 1 in a )
print( 'a' in c )
print( 4 not in a )

#(0)----(N-1),(-N)----(-1)
print(a[0])
a[0]=100
print(a)
print(a[-1])
print(a[-len(a)])

#切片运算
print(a[0:3])
print(a[:3])
print(a[1:])
print(a[:])
print(a[::2])
a[::2] = [0, 0]
print(a)

#比较
a = [1, 2, 3]
b = [1, 2, 3]
c = [1, 2, 3, 4]
d = [3, 2, 1]
print(a == b)
print(a is b)
print(a == c)
print(a is c)
print(a == d)
print(a is d)
print(a < c)
print(a < d)
print(c > d)

"""

#遍历
a = [1, 2, 3, 4, 5]

for i in a:
    print(i)

for i in range(len(a)):
    print(a[i])
