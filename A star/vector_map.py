from matplotlib import patches
import matplotlib.pyplot as plt
from numpy import array as nparray
import time
# ---------------------------------
import collis
# --------------------------------


class Vector_map():
    def __init__(self) -> None:
        vvv = collis.Vector_map()
        self._this = vvv

    def create_circle(self, input: list) -> None:
        if(len(input) != 3):
            raise TypeError
        self._this.create_circle(*input)

    def create_poly(self, input: list) -> None:
        self._this.create_poly(*input)

    def create_border(self, input: list) -> None:
        if(len(input) != 2):
            raise TypeError
        self._this.create_border(*input)

    def delete_shape(self):
        self._this.delete_shape()

    def print_out_data(self) -> None:
        self._this.print_out_data()

    def readfile(self, filename: str, select_type="relative") -> None:
        self._this.readfile(filename, select_type)

    def plot_map(self, ax, alpha=1) -> None:
        temp_list = self._this.get_shape_list()

        for item in temp_list:
            if(isinstance(item, collis.Poly)):
                data = item.get_data()
                data = nparray(data)
                data.resize((int(len(data)/2), 2))
                ax.add_patch(patches.Polygon(data, fc='black', alpha=alpha))
            if(isinstance(item, collis.Circle)):
                data = item.get_data()
                ax.add_patch(patches.Circle(
                    data[1:], data[0], fc='black', alpha=alpha))
            if(isinstance(item, collis.Line)):
                data = item.get_data()
                ax.plot([data[0], data[2]], [data[1], data[3]],
                        color='black', alpha=alpha)

    def scan(self, curr_x, curr_y, r, maxangle, next, get_points=False):
        start = time.time()
        self._this.scan(curr_x, curr_y, r, maxangle, next)
        if(get_points):
            result = self._this.get_result()
            result = nparray(result)
            end = time.time()
            print(f"{end-start} s \n")
            return result

    def scan_one_line(self, curr_x, curr_y, lidar_r, end_x, end_y) -> bool:
        return self._this.scan_one_line(curr_x, curr_y, lidar_r, end_x, end_y)

    def get_nextsteps(self):
        return self._this.get_nextsteps()

    def get_state(self):
        return self._this.get_state()

    def get_area(self):
        return self._this.get_area()

    def get_size(self):
        return self._this.get_size()

    def get_angles(self):
        return self._this.get_angles()

    def get_hit_rate(self):
        return self._this.get_hit_rate()


if __name__ == "__main__":
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot()

    vvv = Vector_map()
    vvv.create_border([10, 10])
    vvv.create_circle([5, 5, 5])
    vvv.plot_map(ax)
    plt.show()
    pass
