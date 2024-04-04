import turtle
from copy import deepcopy


t = turtle.Turtle()
PRINT_HOR_SEP_LEN = 32


def v_offset(v_pos):
    return 250 - v_pos * 100


def h_offset(h_pos):
    return h_pos * 100 - 100


class Point(object):
    """Дырка, через которую продевают шнурок."""
    def __init__(self, pos_vertical, pos_horizontal, next0=None, next1=None):
        self.pos_vertical, self.pos_horizontal = pos_vertical, pos_horizontal
        if pos_vertical == 0:
            next0 = -1  # заглушка для обозначения выхода
        self.nexts = [next0, next1]

    def get_true_nexts(self, exclude_next=None):
        """Возвращает подключенные точки (выход (-1) не учитывается)."""
        ret_list = []
        for next0 in self.nexts:
            if isinstance(next0, Point) and next0 != exclude_next:
                ret_list.append(next0)
        return ret_list

    def get_free_nexts(self):
        """Возвращает количество свободных подключений."""
        ret_value = 0
        for next0 in self.nexts:
            if next0 is None:
                ret_value += 1
        return ret_value

    def repr_pos(self):
        return "Point[{0}][{1}]".format(self.pos_vertical, self.pos_horizontal)
    
    def __repr__(self):
        nexts_reprs = []
        for next0 in self.nexts:
            if isinstance(next0, Point):
                nexts_reprs.append("[{0}][{1}]".format(next0.pos_vertical, next0.pos_horizontal))
            elif next0 is None:
                nexts_reprs.append("")
            else:
                nexts_reprs.append("EXIT")
        
        return "Point[{0}][{1}] -> {2} {3}".format(self.pos_vertical, self.pos_horizontal, nexts_reprs[0], nexts_reprs[1])

    def __eq__(self, other):
        if isinstance(other, Point):
            if (
                self.pos_horizontal == other.pos_horizontal and
                self.pos_vertical == other.pos_vertical
            ):
                return True
        return False


def create_points():
    vertical_list = []
    for j in range(6):  # расположение по вертикали
        horizontal_list = []
        for i in range(2):  # расположение по горизонтали
            horizontal_list.append(Point(j, i))
        vertical_list.append(tuple(horizontal_list))
    return tuple(vertical_list)


def print_points(points):
    for point_tup in points:
        for i, point in enumerate(point_tup):
            repr0 = point.__repr__()
            print(repr0, end="")
            if i != len(point_tup) - 1:
                print(" " * (PRINT_HOR_SEP_LEN - len(repr0)), end="")
        print()


def connect_points(p0, p1):
    """Соединяет две точки."""
    if p0.get_free_nexts() == 0:  # p0 есть оба соседа
        return 1
    if p1.get_free_nexts() == 0:  # p1 есть оба соседа
        return 1

    if p0 == p1:  # нельзя добавить в соседа самого себя
        return 2

    for i in range(2):
        if p0.nexts[i] is None:
            p0.nexts[i] = p1
            break
    
    for i in range(2):
        if p1.nexts[i] is None:
            p1.nexts[i] = p0
            break
    
    return 0


def print_start_state(points, color="black", width=1, draw_points=True):
    t.speed(0)
    t.penup()
    t.hideturtle()
    t.color("black")

    if draw_points:
        for point_tup in points:
            for point in point_tup:
                # t.teleport(point.pos_horizontal * 100, point.pos_vertical * 100)
                h0, v0 = point.pos_horizontal, point.pos_vertical
                t.goto(h_offset(h0), v_offset(v0))
                t.dot()

    t.color(color)
    t.width(width)
    for point_tup in points:
        for point in point_tup:
            h0, v0 = point.pos_horizontal, point.pos_vertical
            for point_next in point.nexts:
                if isinstance(point_next, Point):
                    h1, v1 = point_next.pos_horizontal, point_next.pos_vertical
                    t.goto(h_offset(h0), v_offset(v0))
                    t.pendown()
                    t.goto(h_offset(h1), v_offset(v1))
                    t.penup()


def print_way(way, color="black", width=1):
    t.speed(8)
    t.penup()
    t.hideturtle()

    t.color(color)
    t.width(width)

    for i, point in enumerate(way):
        if i == len(way) - 1:
            break
        point_next = way[i + 1]
        h0, v0 = point.pos_horizontal, point.pos_vertical
        h1, v1 = point_next.pos_horizontal, point_next.pos_vertical
        t.goto(h_offset(h0), v_offset(v0))
        t.pendown()
        t.goto(h_offset(h1), v_offset(v1))
        t.penup()


def restore_way(points):
    """Из матрицы точек восстанавливает путь шнурования от стартовой точки."""
    this_point = points[0][0]
    prev_point = None
    way = [this_point]
    while True:
        new_points = this_point.get_true_nexts(prev_point)
        if len(new_points) == 1:
            way.append(new_points[0])
            prev_point = this_point
            this_point = new_points[0]
        else:
            break
    return way


def search_in_history(found_ways, way):
    """Ищет совпадение пути c уже записанными путями шнуровки."""
    matches_count = 0

    for found_way in found_ways:
        is_matching = True
        if len(found_way) < len(way):
            continue
        for i, point in enumerate(way):
            if point != found_way[i]:
                is_matching = False
                break
        if is_matching:
            matches_count += 1

    return matches_count


def find_next_point_diag(points, this_point: Point, history=[], connect=True):
    """Ищет следующую точку при диагональной шнуровке."""
    len_p = len(points) * len(points[0])
    v0, h0 = this_point.pos_vertical, this_point.pos_horizontal
    h1 = h0 ^ 1  # диагональное плетение, шнурок идёт на другую линию
    for points_tup in points:
        next_point: Point = points_tup[h1]
        v1 = next_point.pos_vertical
        # if next_point in excluded_points:  # если уже исключили эту точку, то не надо
        #     continue
        if v1 == v0:  # диагональное плетение, на том же уровне нельзя
            continue

        way = restore_way(points)
        way.append(next_point)  # обманка для проверки пути в истории
        if search_in_history(history, way):
            way.pop()
            continue
        way.pop()

        if -1 in next_point.nexts:  # если это выходная точка
            if len(way) < len_p - 1:  # можем выйти, только если прошли достаточно точек
                continue

        if next_point.get_free_nexts():  # если есть свободные места подключения, то выбираем её
            if connect:
                connect_points(this_point, next_point)
            return next_point  # нашли нужную точку

    return None  # ничего не подошло


def find_connections(points_create_func):
    all_ways = []
    points_len = points_create_func()
    points_len = len(points_len) * len(points_len[0])

    for _ in range(1000):
        points_copy = points_create_func()
        sp = points_copy[0][0]
        sp_prev = None
        new_way = []

        while True:
            new_way.append(sp)
            if sp.get_free_nexts() == 0:  # некуда подключать точку
                sp_next_s = sp.get_true_nexts(sp_prev)
                if len(sp_next_s) == 1:  # уже задано подключение к точке, переходим по нему
                    sp_prev = sp
                    sp = sp_next_s[0]
                    continue
                break

            sp_next = find_next_point_diag(points_copy, sp, all_ways)
            if sp_next:  # нашли новую точку, подключили
                sp_prev = sp
                sp = sp_next
                continue
            break

        all_ways.append(new_way)

    return [way for way in all_ways if len(way) == points_len]


def create_points_connected():
    points = create_points()
    connect_points(points[1][0], points[2][0])
    connect_points(points[1][1], points[2][1])
    connect_points(points[3][0], points[4][0])
    connect_points(points[3][1], points[4][1])
    connect_points(points[5][0], points[5][1])
    return points


if __name__ == "__main__":
    import time
    example0 = create_points_connected()

    found_ways0 = find_connections(create_points_connected)

    for way0 in found_ways0:
        t.clear()
        print_start_state(example0, "blue", 3, True)
        print_way(way0, "red", 1)
        # input()
        time.sleep(1.5)

    # e = example0
    # way1 = [e[0][0], e[3][1], e[4][1], e[1][0], e[2][0], e[5][1],
    #         e[5][0], e[2][1], e[1][1], e[4][0], e[3][0], e[0][1]]
    #
    # t.clear()
    # print_start_state(e, "blue", 3, True)
    # print_way(way1, "red", 1)

    turtle.exitonclick()  # хз почему пайчарм не видит
