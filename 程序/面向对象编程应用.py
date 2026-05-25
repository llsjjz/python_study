#例子1

import random
from enum import Enum

class Suite(Enum):#Enum类是Python内置的枚举类，可以用来定义一组有名字的常量
    """花色(枚举)"""
    SPADE, HEART, CLUB, DIAMOND = range(4)

class Card:
    """牌"""

    def __init__(self, suite, face):
        self.suite = suite
        self.face = face

    def __repr__(self):#__repr__方法是Python内置的特殊方法，用于定义对象的字符串表示形式，通常用于调试和开发过程中。当我们打印一个对象或者在交互式环境中输入一个对象时，Python会调用该对象的__repr__方法来获取它的字符串表示。
        suites = '♠♥♣♦'
        faces = ['', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']#''用来占位，使得点数1对应A，2对应2，以此类推，13对应K
        return f'{suites[self.suite.value]}{faces[self.face]}'
    
    #__gt__"大于",__lt__"小于",__eq__"等于",__ne__"不等于",__ge__"大于等于",__le__"小于等于"
    def __lt__(self, other):#__lt__方法是Python内置的特殊方法，用于定义对象之间的“小于”比较。当我们使用<运算符比较两个对象时，Python会调用该对象的__lt__方法来进行比较。
        if self.suite == other.suite:
            return self.face < other.face   # 花色相同比较点数的大小
        return self.suite.value < other.suite.value   # 花色不同比较花色对应的值
    
class Poker:
    """扑克"""

    def __init__(self):
        self.cards = [Card(suite, face) 
                      for suite in Suite
                      for face in range(1, 14)]  # 52张牌构成的列表
        self.current = 0  # 记录发牌位置的属性

    def shuffle(self):
        """洗牌"""
        self.current = 0
        random.shuffle(self.cards)  # 通过random模块的shuffle函数实现随机乱序

    def deal(self):
        """发牌"""
        card = self.cards[self.current]
        self.current += 1
        return card

    @property#把一个方法变成属性来访问
    def has_next(self):
        """还有没有牌可以发"""
        return self.current < len(self.cards)
    
class Player:
    """玩家"""

    def __init__(self, name):
        self.name = name
        self.cards = []  # 玩家手上的牌

    def get_one(self, card):
        """摸牌"""
        self.cards.append(card)

    def arrange(self):
        """整理手上的牌"""
        self.cards.sort()

poker = Poker()
poker.shuffle()
players = [Player('东邪'), Player('西毒'), Player('南帝'), Player('北丐')]
# 将牌轮流发到每个玩家手上每人13张牌
for _ in range(13):
    for player in players:
        player.get_one(poker.deal())
# 玩家整理手上的牌输出名字和手牌
for player in players:
    player.arrange()
    print(f'{player.name}: ', end='')#end=''表示print函数输出后不换行，继续在同一行输出
    print(player.cards)


#例子2
from abc import ABCMeta, abstractmethod

class Employee(metaclass=ABCMeta):#ABCMeta是Python内置的抽象基类元类，用于定义抽象基类。抽象基类是一种特殊的类，不能被实例化，只能被继承。它通常包含一个或多个抽象方法，这些方法在抽象基类中没有实现，必须在子类中实现。
    """员工"""

    def __init__(self, name):
        self.name = name

    @abstractmethod#抽象方法是指在抽象基类中定义但没有实现的方法，子类必须实现这些方法才能实例化对象。使用@abstractmethod装饰器来标记一个方法为抽象方法。
    def get_salary(self):
        """结算月薪"""
        pass

class Manager(Employee):
    """部门经理"""

    def get_salary(self):
        return 15000.0


class Programmer(Employee):
    """程序员"""

    def __init__(self, name, working_hour=0):
        super().__init__(name)
        self.working_hour = working_hour

    def get_salary(self):
        return 200 * self.working_hour


class Salesman(Employee):
    """销售员"""

    def __init__(self, name, sales=0):
        super().__init__(name)
        self.sales = sales

    def get_salary(self):
        return 1800 + self.sales * 0.05
    
emps = [Manager('刘备'), Programmer('诸葛亮'), Manager('曹操'), Programmer('荀彧'), Salesman('张辽')]
for emp in emps:
    if isinstance(emp, Programmer):
        emp.working_hour = int(input(f'请输入{emp.name}本月工作时间: '))
    elif isinstance(emp, Salesman):
        emp.sales = float(input(f'请输入{emp.name}本月销售额: '))
    print(f'{emp.name}本月工资为: ￥{emp.get_salary():.2f}元')