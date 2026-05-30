import time


#地图大小
PIXEL_WIDTH = 7  
PIXEL_HEIGHT = 7  

#地图类
class map:
    def __init__(self,ground):
        self.width = PIXEL_WIDTH            #地图宽度
        self.height = PIXEL_HEIGHT          #地图高度
        self.map_false = [[ground] * self.width for _ in range(self.height)]
        self.map_true = [[ground] * self.width for _ in range(self.height)]
        self.map = [[ground] * self.width for _ in range(self.height)]

    def clear(self,ground):
        self.map_false = [[ground] * self.width for _ in range(self.height)]
        self.map_true = [[ground] * self.width for _ in range(self.height)]
        self.map = [[ground] * self.width for _ in range(self.height)]

    def update_map_false(self,element):
        if element.moveable == False:
            for position in element.position:
                if position[0] < self.width and position[1] < self.height:
                    self.map_false[position[1]][position[0]] = element
    
    def update_map_true(self,element):
        if element.moveable == True:
            for position in element.position:
                if position[0] < self.width and position[1] < self.height:
                    self.map_true[position[1]][position[0]] = element

    def update_map(self):
        for height in range(self.height):
            for width in range(self.width):
                if self.map_true[height][width].priority > self.map_false[height][width].priority:
                    self.map[height][width] = self.map_true[height][width]
                else:
                    self.map[height][width] = self.map_false[height][width]

    def get_map(self,mode='all'):
        if mode == 'true':
              for height in range(self.height):
                for width in range(self.width):
                    print(f'{self.map_true[height][width].pattern}',end=' ')
                print()
        elif mode == 'false':
            for height in range(self.height):
                for width in range(self.width):
                    print(f'{self.map_false[height][width].pattern}',end=' ')
                print()
        elif mode == 'all':
            for height in range(self.height):
                for width in range(self.width):
                    print(f'{self.map[height][width].pattern}',end=' ')
                print()

#基本元素类
class element:
    def __init__(self,pattern, priority,moveable,position):
        self.pattern = pattern              #元素图案
        self.priority = priority            #元素优先级，优先级数值越大优先级越高
        self.moveable = moveable            #元素是否可移动 
        self.position = position            #元素位置
        self.len = len(position)            #元素占用的格子数量

    def update_position(self,position):
        self.position = position
 
    def get_position(self):
        return self.position
    
    def move_position(self,aim,position):
        if self.moveable == True:
            if aim in self.position:
                self.position.remove(aim)
                self.position.append(position)


#墙
class wall(element):
    def __init__(self,position):  
        super().__init__(pattern='墙', priority=8,moveable=False,position=position)
#目标
class goal(element):
    def __init__(self,position):
        super().__init__(pattern='点', priority=1,moveable=False,position=position)
#地面
class ground(element):
    def __init__(self):
        super().__init__(pattern='  ', priority=0,moveable=False,position=[])
#箱子
class box(element):
    def __init__(self,position):
        super().__init__(pattern='箱', priority=2,moveable=True,position=position)
#玩家
class player(element):
    def __init__(self,position):
        super().__init__(pattern='我', priority=4,moveable=True,position=position)

#更新地图
def update():
    maps.clear(grounds)
    maps.update_map_false(walls)
    maps.update_map_false(goals)
    maps.update_map_true(boxs)
    maps.update_map_true(player_0)
    maps.update_map()
#移动
def move_true(aim,position):
    if maps.map[aim[1]][aim[0]].priority == 0 or maps.map[aim[1]][aim[0]].priority==1:
        return True
    if maps.map[aim[1]][aim[0]].moveable == False:
        return False
    if maps.map[aim[1]+position[1]][aim[0]+position[0]].priority >= maps.map[aim[1]][aim[0]].priority:
        return False
    if move_true([aim[0]+position[0],aim[1]+position[1]],position)== True:
        maps.map_true[aim[1]][aim[0]].move_position(aim,[aim[0]+position[0],aim[1]+position[1]])
        update()
        return True
    return False
#胜利
def is_win():
    return all(position in goals.position for position in boxs.position)

#元素实例化
grounds = ground()
maps = map(grounds)
walls = wall([[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],
              [1,0],                              [1,6],
              [2,0],                              [2,6],
              [3,0],                              [3,6],
              [4,0],                              [4,6],
              [5,0],                              [5,6],
              [6,0],[6,1],[6,2],[6,3],[6,4],[6,5],[6,6]])
goals = goal([[3,3],[4,3]])
boxs = box([[3,4],[4,4]])
player_0 = player([[3,5]])

position = [0,0]

#更新地图
update()
maps.get_map() 
while True:
    #获取输入
    strings = input('输入wsadq')
    match strings:
        case 'q':
            quit()
        case 'w':
            position[1]=-1
        case 's':
            position[1]=1
        case 'a':
            position[0]=-1
        case 'd':
            position[0]=1
    #更新坐标
    move_true(player_0.position[0],position)
    position[0]=0
    position[1]=0
    #更新地图
    update()
    #获取地图
    maps.get_map() 
    #判断胜利
    if is_win():
        print('win')
        break

    time.sleep(1)


print('结束')


