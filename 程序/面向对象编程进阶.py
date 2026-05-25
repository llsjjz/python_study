#可见性和属性装饰器

#__开头的属性或方法是私有的，外部无法访问
#_开头的属性或方法是受保护的，外部可以访问但不建议访问
class Student:

    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def study(self, course_name):
        print(f'{self.__name}正在学习{course_name}.')


stu = Student('王大锤', 20)
stu.study('Python程序设计')
#print(stu.__name)  # AttributeError: 'Student' object has no attribute '__name'
print(stu._Student__name)#通过属性装饰器实现属性的访问控制


#动态属性

class Student:

    def __init__(self, name, age):
        self.name = name
        self.age = age

stu = Student('王大锤', 20)
stu.sex = '男'  # 给学生对象动态添加sex属性

    #关闭动态属性
class Student:
    __slots__ = ('name', 'age')#定义了__slots__属性后，Student类的对象只能拥有name和age属性，不能再动态添加其他属性了

    def __init__(self, name, age):
        self.name = name
        self.age = age

stu = Student('王大锤', 20)
# AttributeError: 'Student' object has no attribute 'sex'
#stu.sex = '男'


#静态方法和类方法

class Triangle(object):#object是所有类的父类，定义了__new__方法和__init__方法等特殊方法，所有类都继承了这些方法
    """三角形"""

    def __init__(self, a, b, c):
        """初始化方法"""
        self.a = a
        self.b = b
        self.c = c

    @staticmethod
    def is_valid(a, b, c):
        """判断三条边长能否构成三角形(静态方法)"""
        return a + b > c and b + c > a and a + c > b

    # @classmethod
    # def is_valid(cls, a, b, c):
    #     """判断三条边长能否构成三角形(类方法)"""
    #     return a + b > c and b + c > a and a + c > b

    def perimeter(self):
        """计算周长"""
        return self.a + self.b + self.c

    def area(self):
        """计算面积"""
        p = self.perimeter() / 2
        return (p * (p - self.a) * (p - self.b) * (p - self.c)) ** 0.5
      
if Triangle.is_valid(3, 4, 5):#通过类名调用静态方法判断三条边长能否构成三角形,此时对象还没有创建
    t = Triangle(3, 4, 5)
    print(f'周长: {t.perimeter()}')
    print(f'面积: {t.area()}')
else:
    print('无效的边长!!!')

    #补充property属性装饰器
    """property属性装饰器可以把一个方法变成属性来访问，使用@property装饰器修饰的方法就可以通过属性的方式来访问了，不需要加括号了"""
class Triangle(object):
    """三角形"""

    def __init__(self, a, b, c):
        """初始化方法"""
        self.a = a
        self.b = b
        self.c = c

    @staticmethod
    def is_valid(a, b, c):
        """判断三条边长能否构成三角形(静态方法)"""
        return a + b > c and b + c > a and a + c > b

    @property#把一个方法变成属性来访问
    def perimeter(self):
        """计算周长"""
        return self.a + self.b + self.c

    @property
    def area(self):
        """计算面积"""
        p = self.perimeter / 2
        return (p * (p - self.a) * (p - self.b) * (p - self.c)) ** 0.5

if Triangle.is_valid(3, 4, 5):
    t = Triangle(3, 4, 5)
    print(f'周长: {t.perimeter}')
    print(f'面积: {t.area}')
else:
    print('无效的边长!!!')


#继承和多态

class Person:
    """人"""

    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def eat(self):
        print(f'{self.name}正在吃饭.')
    
    def sleep(self):
        print(f'{self.name}正在睡觉.')


class Student(Person):#Student类继承了Person类，Student类是Person类的子类，Person类是Student类的父类，Student类可以使用Person类的属性和方法
    """学生"""
    
    def __init__(self, name, age):
        super().__init__(name, age)#调用父类的构造器来初始化父类的属性
    
    def study(self, course_name):
        print(f'{self.name}正在学习{course_name}.')


class Teacher(Person):#Teacher类继承了Person类，Teacher类是Person类的子类，Person类是Teacher类的父类，Teacher类可以使用Person类的属性和方法
    """老师"""

    def __init__(self, name, age, title):
        super().__init__(name, age)#super()函数是用来调用父类的方法的，super().__init__(name, age)就是调用父类的构造器来初始化父类的属性
        self.title = title#子类特有的属性
    
    def teach(self, course_name):
        print(f'{self.name}{self.title}正在讲授{course_name}.')

stu1 = Student('白元芳', 21)
stu2 = Student('狄仁杰', 22)
tea1 = Teacher('武则天', 35, '副教授')
stu1.eat()
stu2.sleep()
tea1.eat()
stu1.study('Python程序设计')
tea1.teach('Python程序设计')
stu2.study('数据科学导论')