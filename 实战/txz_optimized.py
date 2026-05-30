"""
推箱子小游戏 (Sokoban) - 优化重写版

知识覆盖：
  变量/运算符/分支结构/循环 → 移动逻辑与主循环
  列表/元组/字符串/集合/字典 → 地图表示与关卡存储
  函数(*args, **kwargs, 默认参数) → 各功能函数
  高阶函数(map/filter/sorted) + Lambda → 统计与渲染
  偏函数(functools.partial) → 文件IO快捷函数
  装饰器(@wraps, @property, @staticmethod) → 撤销/属性
  递归调用 → 箱子链检测与移动验证
  面向对象(继承/多态/__slots__/魔术方法) → 元素体系
  枚举(Enum) → 方向与游戏状态
  functools.lru_cache → 边界检查缓存
  functools.reduce + operator → 关卡统计
  文件IO → 关卡存档与读取
"""
import os
import time
import json
from enum import Enum
from functools import wraps, lru_cache, partial, reduce
from operator import add as op_add

# ======================== 枚举 ========================
class Direction(Enum):
    """移动方向枚举，每个成员值为 (dx, dy) 偏移量"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class GameState(Enum):
    """游戏状态枚举"""
    PLAYING = 1
    WON = 2


# ======================== 装饰器 ========================
def undoable(move_func):
    """装饰器：移动前自动保存状态快照，支持撤销功能"""
    @wraps(move_func)
    def wrapper(self, direction, *args, **kwargs):
        # 元组打包快照：(玩家坐标, 冻结的箱子集合, 当前步数)
        snapshot = (self.player_pos, frozenset(self.box_positions), self.steps)
        result = move_func(self, direction, *args, **kwargs)
        if result:
            self._history.append(snapshot)
        return result
    return wrapper


# ======================== 元素类体系(继承 + 多态) ========================
class Element:
    """地图元素基类 —— 使用 __slots__ 限制动态属性，节省内存"""
    __slots__ = ('_symbol', '_priority', '_moveable')

    def __init__(self, symbol: str, priority: int, moveable: bool):
        self._symbol = symbol
        self._priority = priority
        self._moveable = moveable

    @property
    def symbol(self):
        return self._symbol

    @property
    def priority(self):
        return self._priority

    @property
    def moveable(self):
        return self._moveable

    def __repr__(self):
        """魔术方法：print / f-string 时的字符串表示"""
        return self._symbol

    def __lt__(self, other):
        """魔术方法：基于优先级比较（用于图层叠加排序）"""
        return self._priority < other._priority

    def __eq__(self, other):
        if isinstance(other, Element):
            return self._symbol == other._symbol
        return False

    def __hash__(self):
        return hash(self._symbol)


class Wall(Element):
    """墙 —— 不可移动，最高优先级"""
    def __init__(self):
        super().__init__('墙', priority=8, moveable=False)


class Goal(Element):
    """目标点 —— 不可移动，低优先级"""
    def __init__(self):
        super().__init__('点', priority=1, moveable=False)


class Ground(Element):
    """地面 —— 不可移动，最低优先级"""
    def __init__(self):
        super().__init__('  ', priority=0, moveable=False)


# 全局单例，避免重复创建
_WALL = Wall()
_GOAL = Goal()
_GROUND = Ground()


# ======================== 地图类 ========================
class GameMap:
    """游戏地图，管理静态图层与渲染"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # 列表生成式：二维列表表示地图
        self._static = [[_GROUND] * width for _ in range(height)]
        self._render = [[_GROUND] * width for _ in range(height)]

    def place_walls(self, positions):
        """放置墙壁（接收坐标列表）"""
        for x, y in positions:
            if 0 <= x < self.width and 0 <= y < self.height:
                self._static[y][x] = _WALL

    def place_goals(self, positions):
        """放置目标点"""
        for x, y in positions:
            if 0 <= x < self.width and 0 <= y < self.height:
                self._static[y][x] = _GOAL

    def update_render(self, player_pos: tuple, box_positions: set, goal_positions: set):
        """更新渲染图层 —— 处理元素叠加与特殊符号显示"""
        # 切片复制静态层
        self._render = [row[:] for row in self._static]

        # 渲染箱子（若在目标点上则显示"归"）
        for bx, by in box_positions:
            on_goal = (bx, by) in goal_positions
            self._render[by][bx] = Element('归', 5, True) if on_goal else Element('箱', 2, True)

        # 渲染玩家（若在目标点上则显示"达"）
        px, py = player_pos
        on_goal = (px, py) in goal_positions
        self._render[py][px] = Element('达', 6, True) if on_goal else Element('我', 4, True)

    @property
    def display(self):
        """@property: 以属性方式获取完整的地图字符串"""
        return '\n'.join(
            ' '.join(str(cell) for cell in row)
            for row in self._render
        )

    def render(self):
        """清屏并输出地图到控制台"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.display)

    def __getitem__(self, index):
        """魔术方法：支持 game_map[y][x] 索引访问静态层"""
        return self._static[index]

    def __contains__(self, pos):
        """魔术方法：支持 (x, y) in game_map 判断坐标是否在地图内"""
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height


# ======================== 边界检查(lru_cache 缓存) ========================
@lru_cache(maxsize=256)
def _in_bounds(x: int, y: int, width: int, height: int) -> bool:
    """独立函数 + lru_cache：缓存重复的边界检查结果"""
    return 0 <= x < width and 0 <= y < height


# ======================== 关卡数据(字典嵌套 + 元组坐标) ========================
# 所有关卡均已人工验证为可解
LEVELS = {
    1: {
        'name': '第一关 · 初入仓库',
        'width': 7, 'height': 7,
        'walls': [
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
            (0, 1), (6, 1),
            (0, 2), (6, 2),
            (0, 3), (6, 3),
            (0, 4), (6, 4),
            (0, 5), (6, 5),
            (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6),
        ],
        'goals': [(3, 3), (4, 3)],
        'boxes': [(3, 4), (4, 4)],
        'player': (3, 5),
    },
    2: {
        'name': '第二关 · 左右开弓',
        'width': 7, 'height': 7,
        'walls': [
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
            (0, 1), (6, 1),
            (0, 2), (6, 2),
            (0, 3), (6, 3),
            (0, 4), (6, 4),
            (0, 5), (6, 5),
            (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6),
        ],
        # 解法: 推(3,4)↑到(3,3)→去(2,2)→推(3,2)→到(4,2)→推(4,2)→到(5,2)
        'goals': [(3, 3), (5, 2)],
        'boxes': [(3, 4), (3, 2)],
        'player': (3, 5),
    },
    3: {
        'name': '第三关 · 三箱归位',
        'width': 7, 'height': 7,
        'walls': [
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
            (0, 1), (6, 1),
            (0, 2), (6, 2),
            (0, 3), (6, 3),
            (0, 4), (6, 4),
            (0, 5), (6, 5),
            (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6),
        ],
        # 解法: 推(3,2)↓三次到(3,5)→推(2,3)←到(1,3)→推(5,3)→到(6,3)
        'goals': [(3, 5), (1, 3), (6, 3)],
        'boxes': [(3, 2), (2, 3), (5, 3)],
        'player': (3, 1),
    },
}


# ======================== 游戏主类 ========================
class Sokoban:
    """推箱子游戏控制器 —— 集中管理游戏状态与逻辑"""

    def __init__(self, level_id: int = 1):
        self._history: list = []          # 撤销历史栈（列表）
        self.box_positions: set = set()    # 箱子坐标集合
        self.goal_positions: set = set()   # 目标坐标集合
        self.player_pos: tuple = (0, 0)    # 玩家坐标元组
        self.steps: int = 0                # 步数计数器
        self.state: GameState = GameState.PLAYING
        self.level_id = level_id
        self._load_level(level_id)

    # ---- 关卡加载 ----
    def _load_level(self, level_id: int):
        """从字典中加载指定关卡的数据"""
        level = LEVELS.get(level_id, LEVELS[1])
        self.level_name = level['name']
        self._game_map = GameMap(level['width'], level['height'])

        # 放置静态元素
        self._game_map.place_walls(level['walls'])
        self._game_map.place_goals(level['goals'])

        # 初始化动态状态（列表 → 集合；集合查找为 O(1)）
        self.box_positions = set(level['boxes'])
        self.goal_positions = set(level['goals'])
        self.player_pos = level['player']
        self.steps = 0
        self._history.clear()
        self.state = GameState.PLAYING
        self._refresh()

    def _refresh(self):
        """通知地图刷新渲染层"""
        self._game_map.update_render(
            self.player_pos, self.box_positions, self.goal_positions
        )

    # ---- 静态工具方法 ----
    @staticmethod
    def _move_point(pos: tuple, d: Direction) -> tuple:
        """@staticmethod: 坐标运算 —— 元组解包再打包"""
        x, y = pos
        dx, dy = d.value
        return (x + dx, y + dy)

    def _is_blocked(self, pos: tuple) -> bool:
        """检查某位置是否被墙壁阻挡（边界外也视为阻挡）"""
        x, y = pos
        if not _in_bounds(x, y, self._game_map.width, self._game_map.height):
            return True
        # 利用 __getitem__ 魔术方法：game_map[y][x]
        return self._game_map[y][x] is _WALL

    # ---- 箱子链检测(递归) ----
    def _get_box_chain(self, start: tuple, direction: Direction) -> list:
        """
        递归收集沿 direction 方向连续排列的箱子坐标链
        基准条件：start 位置无箱子 → 返回空列表 []
        递归条件：start 位置有箱子 → [start] + 继续检查下一格
        """
        if start not in self.box_positions:
            return []
        next_pos = self._move_point(start, direction)
        return [start] + self._get_box_chain(next_pos, direction)

    # ---- 移动逻辑(装饰器 @undoable 自动记录历史) ----
    @undoable
    def move(self, direction: Direction) -> bool:
        """执行玩家移动，含推箱子处理。返回 True 表示移动成功"""
        new_pos = self._move_point(self.player_pos, direction)

        # 墙壁阻挡检查
        if self._is_blocked(new_pos):
            return False

        # 需要推箱子？
        if new_pos in self.box_positions:
            chain = self._get_box_chain(new_pos, direction)
            if not chain:
                return False

            # 检查箱子链末端的下一格是否可进入
            end_next = self._move_point(chain[-1], direction)
            if self._is_blocked(end_next):
                return False
            # 额外检查：连锁推动时，末端下一格不能也有箱子
            if end_next in self.box_positions:
                return False

            # 从远到近依次移动每个箱子（切片 [::-1] 反转列表）
            for box in chain[::-1]:
                self.box_positions.remove(box)
                self.box_positions.add(self._move_point(box, direction))

        # 移动玩家
        self.player_pos = new_pos
        self.steps += 1
        self._refresh()
        return True

    # ---- 撤销 ----
    def undo(self) -> bool:
        """撤销上一步（通过历史栈恢复状态）—— 元组解包还原"""
        if not self._history:
            return False
        self.player_pos, frozen_boxes, self.steps = self._history.pop()
        self.box_positions = set(frozen_boxes)  # frozenset → set
        self._refresh()
        return True

    # ---- 属性计算(@property) ----
    @property
    def is_won(self):
        """@property: 所有箱子位置与目标位置重合即为胜利（集合 == 比较）"""
        return self.box_positions == self.goal_positions

    @property
    def boxes_done(self):
        """已到位箱子数（集合交集 & 运算）"""
        return len(self.box_positions & self.goal_positions)

    # ---- 统计信息(使用高阶函数 map + lambda) ----
    def get_stats(self) -> dict:
        """返回当前游戏统计字典"""
        return {
            '步数': self.steps,
            '箱子进度': f'{self.boxes_done}/{len(self.goal_positions)}',
            '可撤销': len(self._history),
        }

    def render(self):
        self._game_map.render()

    def __repr__(self):
        return f'Sokoban(level={self.level_id}, steps={self.steps})'


# ======================== 文件IO ========================
# 偏函数(functools.partial)：绑定编码参数，创建快捷函数
write_json = partial(json.dump, ensure_ascii=False, indent=2)
_load_dict = partial(json.load)


def save_levels(filepath: str, levels: dict) -> bool:
    """将关卡数据保存为 JSON 文件（文件IO - 写入）"""
    try:
        # 字典生成式：将 tuple 坐标转为 list（JSON 不支持 tuple）
        serializable = {}
        for lid, lv in levels.items():
            serializable[str(lid)] = {
                k: ([list(p) for p in v] if k in ('walls', 'goals', 'boxes')
                    else (list(v) if k == 'player' else v))
                for k, v in lv.items()
            }
        with open(filepath, 'w', encoding='utf-8') as f:
            write_json(serializable, f)
        return True
    except OSError as e:
        print(f'保存失败: {e}')
        return False


def load_levels(filepath: str) -> dict:
    """从 JSON 文件加载关卡数据（文件IO - 读取）—— 字典生成式还原 tuple"""
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = _load_dict(f)

    # 字典生成式 + 条件表达式：将 list 转回 tuple
    result = {}
    for lid, lv in raw.items():
        result[int(lid)] = {
            k: ([tuple(p) for p in v] if k in ('walls', 'goals', 'boxes')
                else (tuple(v) if k == 'player' else v))
            for k, v in lv.items()
        }
    return result


# ======================== 输入处理 ========================
# 字典：按键 → 方向
KEY_DIR = {
    'w': Direction.UP,    'W': Direction.UP,
    's': Direction.DOWN,  'S': Direction.DOWN,
    'a': Direction.LEFT,  'A': Direction.LEFT,
    'd': Direction.RIGHT, 'D': Direction.RIGHT,
}

# Lambda 表达式：方向 → 中文名称
DIR_NAME = lambda d: {
    Direction.UP: '上', Direction.DOWN: '下',
    Direction.LEFT: '左', Direction.RIGHT: '右',
}.get(d, '?')


# ======================== 主程序入口 ========================
def main():
    """游戏主循环"""
    # ANSI 转义序列颜色常量（字符串应用）
    CYAN, YELLOW, GREEN, RED, RESET = '\033[36m', '\033[33m', '\033[32m', '\033[31m', '\033[0m'

    # 使用 functools.reduce + operator.add 计算总目标数（高阶函数演示）
    total_goals = reduce(op_add, (len(lv['goals']) for lv in LEVELS.values()), 0)

    current = 1
    total_levels = len(LEVELS)
    game = Sokoban(current)

    print(f'{CYAN}====== 推箱子 Sokoban ======{RESET}')
    print(f'共 {total_levels} 个关卡，总计 {total_goals} 个目标箱子')
    print('W/S/A/D 移动 | Q 退出 | U 撤销 | R 重来 | N 下一关')
    time.sleep(0.8)

    while True:
        game.render()

        # 显示关卡名和统计（f-string + 字典遍历）
        print(f'{CYAN}=== {game.level_name} ==={RESET}')
        stats = game.get_stats()
        # map + lambda：将字典每项格式化为 "键: 值" 字符串
        stat_text = ' | '.join(map(lambda kv: f'{kv[0]}: {kv[1]}', stats.items()))
        print(stat_text)
        print(f'{YELLOW}输入操作:{RESET} ', end='')

        key = input().strip()

        # match/case 模式匹配（Python 3.10+）
        match key.lower():
            case 'q':
                print('游戏结束，再见！')
                break

            case 'u':
                if game.undo():
                    print('已撤销上一步')
                else:
                    print(f'{RED}没有可撤销的操作{RESET}')
                time.sleep(0.25)

            case 'r':
                game = Sokoban(current)
                print('重新开始')
                time.sleep(0.3)

            case 'n':
                current = current % total_levels + 1
                game = Sokoban(current)
                print(f'进入第{current}关')
                time.sleep(0.3)

            case _:
                direction = KEY_DIR.get(key)
                if direction is None:
                    print('无效按键，使用 W/S/A/D 移动')
                    time.sleep(0.3)
                    continue

                if game.move(direction):
                    # 移动成功 → 检查胜利
                    if game.is_won:
                        game.state = GameState.WON
                else:
                    print(f'{RED}无法向{DIR_NAME(direction)}移动{RESET}')
                    time.sleep(0.25)

        # 胜利处理（分支结构）
        if game.state == GameState.WON:
            game.render()
            print(f'{GREEN}{"=" * 32}{RESET}')
            print(f'{GREEN}    通关！共用了 {game.steps} 步{RESET}')
            print(f'{GREEN}{"=" * 32}{RESET}')

            if current < total_levels:
                choice = input('进入下一关？(y/N): ').strip().lower()
                if choice == 'y':
                    current += 1
                    game = Sokoban(current)
                else:
                    break
            else:
                print(f'{YELLOW}全部 {total_levels} 关已通关！{RESET}')
                break


if __name__ == '__main__':
    main()
