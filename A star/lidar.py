from time import time
import numpy as np
from math import sin, cos, pi, acos, fabs
import matplotlib.pyplot as plt
from matplotlib import patches
# --------------
from vector_map import Vector_map
from shape import Line, Circle


class lidar():
    '''
    __init__() :  self,curr_point,dest_point,radius,precision
    content:    curr_point,  radius,  precision,
                circular_vetor_list,  point_list,  
                area_list,  angle_list,nextsteps_list,  history
    '''

    def __init__(self, curr_point, destination, radius,  filename=None, relative=True, input_map=None):
        '''
        if want to use the mapfile which is alread read:
            use 'input_map'
        or you want __init__ to read a file
            use 'filename' and 'relative'(type)
        '''
        # --
        self.score = None
        self.look_backward = None
        self.buff_next = None

        # --
        if(type(curr_point) == list):
            curr_point = tuple(curr_point)
        if(type(destination) == list):
            destination = tuple(destination)

        self._curr_point = curr_point
        self._dest_point = destination
        self._pre_point = None
        self._step = 0
        self._radius = radius
        self._initial_r = radius
        self._wander = 0
        self._state = None
        self._distance = 0
        # ---
        self._point_list = None
        self._area_list = None
        self._angle_list = []
        self._nextsteps_list = None
        self._history = [(curr_point[0], curr_point[1], radius)]
        self._wave = []
        # -----
        if(input_map == None):
            if(filename == None):
                raise TypeError
            self.readfile(filename, relative)
        else:
            self._map = input_map

    def setter(self, type_name, input):
        '''
        type_name=cp,r,wander
        '''
        if(type_name == 'cp'):
            if(type(input) != tuple and type(input) != list):
                raise TypeError
            self._curr_point = tuple(input)
            self.add_history(tuple(input))
        elif(type_name == 'r'):
            if(type(input) == float or type(input) == int):
                self._radius = input
            else:
                raise TypeError
        elif(type_name == 'wander'):
            if(type(input) == int):
                self._wander = input
            else:
                raise TypeError
        else:
            raise TypeError

    def getter_single(self, type_name):
        '''
        type_name=cp,d,step,r,pre,wander,state,distance,initial_r
        '''
        if(type_name == 'cp'):
            return tuple(self._curr_point)
        elif(type_name == 'd'):
            return tuple(self._dest_point)
        elif(type_name == 'step'):
            return self._step
        elif(type_name == 'r'):
            return self._radius
        elif(type_name == 'pre'):
            return self._pre_point
        elif(type_name == 'wander'):
            return int(self._wander)
        elif(type_name == 'state'):
            return self._state
        elif(type_name == 'distance'):
            return self._distance
        elif(type_name == 'initial_r'):
            return self._initial_r
        else:
            raise TypeError

    def getter_list(self, type_name):
        '''
        'point', 'area', 'angle', 'next', 'history'
        '''
        if(type_name == 'point'):
            return tuple(self._point_list)
        elif(type_name == 'area'):
            return tuple(self._area_list)
        elif(type_name == 'angle'):
            return tuple(self._angle_list)
        elif(type_name == 'next'):
            return tuple(self._nextsteps_list)
        elif(type_name == 'history'):
            return tuple(self._history)
        else:
            raise TypeError

    def if_in_dest(self):
        curr = self._curr_point
        dest = self._dest_point
        if(curr[0] == dest[0] and curr[1] == dest[1]):
            return True
        else:
            return False

    def run_times_equalmore_than(self, num: int) -> bool:
        if(self._step >= num):
            return True
        else:
            return False

    def plot_map(self, ax, alpha=1):
        self._map.plot_map(ax, alpha)

    def plot_his(self, ax, alpha=1):
        # plot map
        self.plot_map(ax, alpha)
        his = np.array(self._history)

        # plot lidar range
        for i in range(len(his)):
            ax.add_patch(patches.Circle(
                [his[i, 0], his[i, 1]], his[i, 2], ec='r', fc='none', alpha=alpha))

        # plot path
        ax.plot(his[:, 0], his[:, 1], color='orange')

        # plot start point and text
        ax.scatter(his[0][0], his[0][1], color='purple')
        ax.text(his[0][0], his[0][1], "start",
                ha='right', va='bottom', fontsize=8, color='purple', fontstyle='italic')

        # plot midway point
        ax.scatter(his[1:, 0], his[1:, 1], color='orange')

        # plot dest point and text
        dest_point = self.getter_single('d')
        ax.scatter(dest_point[0], dest_point[1], color='purple')
        ax.text(dest_point[0], dest_point[1], "destination",
                ha='right', va='bottom', fontsize=8, color='purple', fontstyle='italic')

    def plot_wave(self, ax):
        d_list = self._wave

        i_list = [i for i in range(0, len(d_list), 1)]
        ax.plot(i_list, d_list, color='orange')

    def plot_scan_range(self, ax, alpha=1):
        curr = tuple(self._curr_point)

        r = self._radius
        self.plot_map(ax, alpha)

        ax.axis([curr[0]-r-0.5, curr[0]+r+0.5, curr[1]-r-0.5, curr[1]+r+0.5])

        ax.scatter(curr[0], curr[1], color='purple')

        ax.add_patch(patches.Circle(
            curr, r, ec='r', fc='none'))  # lidar range

    def plot_score(self, ax):
        if (self.score != None):
            for item in self.score:
                ax.text(item[4], item[5], f't={item[0]}\na={item[1]}\nb={item[2]}\nc={item[3]}',
                        ha='right', va='bottom', fontsize=10, color='blue')

    def plot_accessible_area(self, ax, alpha=1):
        curr = tuple(self._curr_point)

        dest = tuple(self._dest_point)
        area = tuple(self._area_list)
        next = tuple(self._nextsteps_list)
        r = self._radius

        self.plot_scan_range(ax, alpha)
        self.plot_map(ax, alpha)  # map

        if(next != None and next != ()):
            nn = np.array(next)
            ax.scatter(nn[:, 0], nn[:, 1], color='orange')  # next_steps

        for i in range(0, len(area)-1, 2):  # area border
            shape = patches.Polygon(
                [curr, area[i], area[i+1]], ec='g', fc='g', alpha=0.3)
            ax.add_patch(shape)

        ax.scatter(dest[0], dest[1], color='purple')  # dest
        ax.text(dest[0], dest[1], "destination",
                ha='right', va='bottom', fontsize=8, color='purple', fontstyle='italic')

    def readfile(self, filename, relative=True):
        if(type(filename) != str):
            raise TypeError
        else:
            self._map = Vector_map()
            if(relative):
                self._map.readfile(filename)
            else:
                self._map.readfile(filename, "1")

    def scan(self, maxangle=60, next='m', get_points=False, get_angle=False):
        self.score = None
        self.look_backward = None

        self._point_list = self._map.scan(
            *self._curr_point, self._radius, maxangle, next, get_points=get_points)
        self._state = self._map.get_state()
        self._hit_rate = self._map.get_hit_rate()
        print(f"state: {self._state}")
        if(get_angle):
            self._angle_list = self._map.get_angles()

        if(self._state == 'n'):
            self._area_list = self._map.get_area()
            self._nextsteps_list = self._map.get_nextsteps()
        else:
            self._area_list = []
            self._nextsteps_list = []

    def scan_one_line(self, end_point) -> bool:
        return self._map.scan_one_line(*self._curr_point, self._radius, *end_point)

    def add_wave(self):
        curr = self.getter_single("cp")
        end = self.getter_single("d")
        wave = self._wave

        new_line = Line([curr, end])
        new_d = new_line.length()
        self._wave.append(new_d)

        len_wave = len(wave)

        if(len_wave > 4):

            wave_pre1 = Line([(len_wave-3, wave[len_wave-3]),
                              (len_wave-2, wave[len_wave-2])])

            wave_pre2 = Line([(len_wave-2, wave[len_wave-2]),
                             (len_wave-1, wave[len_wave-1])])
            new_d = new_line.length()

            slope1 = wave_pre1.find_slope()
            slope2 = wave_pre2.find_slope()

            d_min = min(wave)

            if(slope1*slope2 < 0):
                self._wander += 1

            if(new_d <= d_min):
                self._wander = 0

            print(f"wander: {self._wander}")

        del new_line

    def add_history(self, point):
        his = self._history.copy()
        pre_point = (his[len(his)-1][0], his[len(his)-1][1])

        temp = Line([[*pre_point], [*point]])
        self._distance += temp.length()
        del temp

        self._pre_point = (pre_point[0], pre_point[1])
        his.append(
            (point[0], point[1], self._radius))

        self._history = his
        self._step += 1
        self.add_wave()

    def set_next_go(self, data):
        if(type(data) == tuple or type(data) == list):
            self.buff_next = tuple(data)
        else:
            raise TypeError

    def go(self):
        if(self.buff_next != None):
            self._curr_point = self.buff_next
            self.add_history(self.buff_next)
            self.buff_next = None

    def add_gray_circle(self):
        his = self._history
        curr = self._curr_point
        curr_range = Circle([self._radius, *curr])

        if(len(his) > 5):
            for item in his[-5:-2]:
                temp = Circle([item[2], item[0], item[1]])
                if(not curr_range.in_region(temp)):
                    self._map.create_circle([item[2], item[0], item[1]])

    def find_the_best_r(self):
        large = self._initial_r*3
        while(1):
            self.scan()
            if(self._state == 'b'):
                self._radius -= large
            elif(self._state == 'n' and len(self._area_list)/2 == 1):
                return self._radius

            else:
                self._radius += large

    def clear_scan_result(self):
        self._area_list = []
        self._nextsteps_list = []
        self._angle_list = []
        self._point_list = []
        self.score = []
        self.look_backward = []
        self._state = None
