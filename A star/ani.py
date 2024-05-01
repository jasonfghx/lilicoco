from numpy import array as nparray
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import patches
# ---
from lidar import lidar
from vector_map import Vector_map


def run_collis(i, each_angle, arrow):
    x, y = each_angle[i][0], each_angle[i][1]
    arrow.set_data(dx=float(x), dy=float(y))
    return arrow,


def ani_collis(fig, ax, lidar_obj):

    curr = lidar_obj.getter_single('cp')
    r = lidar_obj.getter_single('r')

    plt.axis([curr[0]-r-2, curr[0]+r+2, curr[1]-r-2, curr[1]+r+2])

    points = lidar_obj.getter_list('point')
    each_angle = [[item[0]-curr[0], item[1]-curr[1]] for item in points]

    lidar_obj.plot_map(ax)
    ax.add_patch(patches.Circle(curr, r, ec='r', fc='none'))
    plt.scatter(curr[0], curr[1], color='red')

    arrow = plt.arrow(curr[0], curr[1], 0, 0, width=0.03, color='r')
    arrow.set_data(dx=each_angle[0][0], dy=each_angle[0][1])

    each_angle = nparray(each_angle)
    anii = animation.FuncAnimation(fig, run_collis, frames=len(each_angle), fargs=(
        each_angle, arrow), interval=0.001/len(each_angle), blit=True)
    plt.show()
    return anii


if __name__ == "__main__":
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot()
    fig.tight_layout()
    fig.suptitle('Lidar scan', fontsize=12)
    vvv = Vector_map()
    vvv.readfile("one_circle.txt")
    robot = lidar([10.136201155616492, 8.558357538949034], [
                  20.219444716482226, 16.087272247161337], 3.8003, input_map=vvv)
    robot.scan(get_points=True, get_angle=True)
    # robot.plot_accessible_area(ax)
    # plt.savefig('available_area_testmap_1310.png')
    # plt.show()
    ani_collis(fig, ax, robot)  # .save('animation.gif', writer='Pillow')
