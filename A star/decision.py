from shape import *
from lidar import lidar
from vector_map import Vector_map
from math import isnan


def is_reachable(lidar_obj: lidar) -> int:
    lidar_obj.go()
    # hit is True
    if(lidar_obj.scan_one_line(lidar_obj.getter_single('d'))):
        return 0
    else:
        return 1


def go_to_dest(lidar_obj: lidar) -> int:
    lidar_obj.setter('cp', lidar_obj.getter_single('d'))
    return 2


def is_all_white(lidar_obj: lidar) -> int:
    if(lidar_obj.getter_single("state") == 'w'):
        return 1
    else:
        return 0


def lager_radius(lidar_obj: lidar) -> int:
    r = lidar_obj.getter_single('r')
    lidar_obj.setter('r', r*2)
    lidar_obj.clear_scan_result()
    return 0


def scan_and_is_wander(lidar_obj: lidar) -> int:
    lidar_obj.scan(60, 'm')
    if(lidar_obj.getter_single('wander') > 3):
        lidar_obj.setter('wander', 0)
        return 1
    else:
        return 0


def is_all_black(lidar_obj: lidar) -> int:
    if(lidar_obj.getter_single('state') == 'b'):
        return 1
    else:
        return 0


def smaller_radius(lidar_obj: lidar) -> int:
    r = lidar_obj.getter_single('r')
    lidar_obj.setter('r', r*0.5)
    return 0


def go_the_shortest(lidar_obj: lidar) -> int:
    r = lidar_obj.getter_single('r')
    cp = lidar_obj.getter_single('cp')
    end = lidar_obj.getter_single('d')

    temp = Circle([r, *cp])
    p_point = temp.project_to_circle(end)

    lidar_obj.set_next_go(p_point)
    return 0


def is_nextstep_one(lidar_obj: lidar) -> int:
    next_step = lidar_obj.getter_list('next')

    if(len(next_step) == 1):
        return 1
    else:
        return 0


def rating_and_the_smallest_is_one(lidar_obj: lidar) -> int:
    next_step = lidar_obj.getter_list('next')
    pre_point = lidar_obj.getter_single('pre')
    curr_point = lidar_obj.getter_single('cp')
    dest_point = lidar_obj.getter_single('d')

    score = get_abct_and_sorting(next_step, pre_point, curr_point, dest_point)

    lidar_obj.score = score

    try:
        if(score.count(score[0]) == 1):
            return 1
        else:
            return 0
    except:
        raise IndexError


def go_to_the_only_nextstep(lidar_obj: lidar) -> int:
    next_step = lidar_obj.getter_list('next')
    lidar_obj.set_next_go(next_step[0])
    return 0


def look_backward_and_is_newlist_one(lidar_obj: lidar) -> int:
    score = lidar_obj.score

    look_backward = []
    for item in score:
        point = [item[4], item[5]]

        if(lidar_obj.scan_one_line(point)):
            look_backward.append(point)

    lidar_obj.look_backward = look_backward

    if(len(look_backward) == 1):
        return 1
    else:
        return 0


def choose_best_look_backward(lidar_obj: lidar) -> int:
    lidar_obj.set_next_go(lidar_obj.look_backward[0])
    return 0


def choose_best_abc_order(lidar_obj: lidar) -> int:
    try:
        lidar_obj.set_next_go((lidar_obj.score[0][4], lidar_obj.score[0][5]))
        print(f"choose:{(lidar_obj.score[0][4], lidar_obj.score[0][5])}\n")
    except:
        raise OverflowError
    return 0


def choose_the_worsest_abc_order(lidar_obj: lidar) -> int:
    rating_and_the_smallest_is_one(lidar_obj)
    score = lidar_obj.score
    lidar_obj.set_next_go([score[-1][4], score[-1][5]])

# ------------------------------------------


def check_dir(line1: Line, line2: Line):

    try:
        angle = line1.angle_btw_line(line2)

        if(0 <= angle < 45):
            return 1
        elif(45 <= angle < 90):
            return 5
        elif(90 <= angle < 135):
            return 7
        else:
            return 9
    except:
        raise OverflowError


def get_abct_and_sorting(next_step, pre_point, curr_point, dest_point):
    a_list = []
    b_list = []
    c_list = []

    curr = Point(curr_point)
    dest = Point(dest_point)

    curr_to_dest = curr-dest

    if(pre_point != None):
        pre = Point(pre_point)
        pre_line = pre-curr
    else:
        pre = None

    i = 0

    for item in next_step:
        item_point = Point(item)
        if(pre != None):
            check_line = curr-item_point
            b = check_dir(pre_line, check_line)

        else:
            b = 0

        line_to_dest = item_point-dest

        a = line_to_dest.length()

        c = curr_to_dest.distance_point2line(item)

        a_list.append(a)
        b_list.append(b)
        c_list.append(c)

    del curr, dest
    return sorting(next_step, a_list, b_list, c_list)


def sorting(next_step: list, a_list: list, b_list: list, c_list: list):
    score = []

    a_list = process_list_with_mapping(a_list)
    c_list = process_list_with_mapping(c_list)
    i = 0

    for a, b, c in zip(a_list, b_list, c_list):
        t = a+b+c
        score.append([t, a, b, c, next_step[i]
                     [0], next_step[i][1]])
        i += 1

    score = sorted(score, key=lambda x: (x[0], x[1], x[2], x[3]))

    return score


def process_list_with_mapping(data: list) -> list:
    sorted_lst = sorted(data)

    mapping = {}
    for i, val in enumerate(sorted_lst):
        if val not in mapping:
            mapping[val] = i+1

    new_lst = [mapping[val] for val in data]
    new_lst = [int(val) for val in new_lst]

    return new_lst
