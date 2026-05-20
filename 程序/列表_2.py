import random

#列表的添加和删除
'''
#添加
list1 = [1,2,3]
list1.append(4)
print(list1)
list1.insert(0,0)
print(list1)
#删除
list2 = [1,2,3,4,5]
if 3 in list2:
    list2.remove(3)
print(list2)
list2.pop()#默认删除最后一个元素
print(list2)
a = list2.pop(1)
print(a)
list2.append(a)
print(list2)
del list2[0]#删除指定位置的元素
print(list2)
list2.clear()
print(list2)

list2 = [1,2,1,4,1]
if 1 in list2:
    list2.remove(1)#只会删除第一个1
print(list2)
'''

#位置和频率
'''
list3 = [1,2,3,4,5,1,2,3]
print(list3.index(1))#返回第一个1的索引
print(list3.index(1,1))#从索引1开始查找第一个1的索引
print(list3.index(1,2))#从索引2开始查找第一个1的索引
print(list3.count(1))#返回1的个数
'''

#元素排序和反转
'''
list4 = ['cas', 'adsa', 'dads', 'basd', 'e']
list4.sort()#默认升序排序
print(list4)
list4.reverse()#反转列表
print(list4)
'''
#列表嵌套
'''
list5 = [[1,2,3],[4,5,6],[7,8,9]]
print(list5[0])#访问第一个子列表
print(list5[0][0])#访问第一个子列表的第一个元素
print(list5[1][2])#访问第二个子列表的第三个元素
'''

#列表的生成
a = [i for i in range(10)]
print(a)
b = [i**2 for i in range(10)]
print(b)

c = [[random.randint(1,100) for i in range(5)]for j in range(3)]#生成一个3行5列的二维列表，每个元素是1到100之间的随机整数
print(c)

c = []
for j in range(3):
    row = []
    for i in range(5):
        row.append(random.randint(1,100))
    c.append(row)
print(c)




