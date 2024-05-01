from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os
import sys
# -----------------------
from decision_tree import lidar_Controller
from lidar import lidar
from vector_map import Vector_map


def go_thru(input_map, start, destination, radius, ax, ax2, ax3, canvas, canvas2, canvas3):
    Controller = lidar_Controller()
    robot = lidar(start, destination, radius, input_map=input_map)
    end_type = "None"

    while(not robot.if_in_dest()):
        if(robot.run_times_equalmore_than(150)):
            print("Time Out!")
            end_type = "time_out"
            break
        else:
            Controller.run(robot)

            clear_canvas(ax, ax2, ax3)

            robot.plot_his(ax, alpha=0.5)
            robot.plot_accessible_area(ax2, alpha=0.5)
            robot.plot_wave(ax3)
            robot.plot_score(ax2)

            canvas_draw(canvas, canvas2, canvas3)

    if(end_type != "time_out"):
        end_type = "done"

    clear_canvas(ax, ax2, ax3)

    robot.plot_his(ax, alpha=0.5)
    robot.plot_wave(ax3)
    plot_the_final(ax2, robot, end_type)
    canvas_draw(canvas, canvas2, canvas3)
    print(robot.getter_single("distance"))

    return True


def go_step_by_step(lidar_obj: lidar, controller: lidar_Controller, ax, ax2, ax3, canvas, canvas2, canvas3):
    step_count = lidar_obj.getter_single("step")
    print(f"### step {step_count}\n")

    #print(f'c:{curr} pre:{pre}\n')

    clear_canvas(ax, ax2, ax3)

    if(lidar_obj.if_in_dest()):
        plot_the_final(ax2, lidar_obj, "done")
        lidar_obj.plot_wave(ax3)
        canvas_draw(canvas, canvas2, canvas3)
        return "done"
    elif(lidar_obj.run_times_equalmore_than(150)):
        plot_the_final(ax2, lidar_obj, "time_out")
        lidar_obj.plot_wave(ax3)
        canvas_draw(canvas, canvas2, canvas3)
        return "time_out"
    else:
        controller.run(lidar_obj)

        lidar_obj.plot_his(ax, alpha=0.5)
        lidar_obj.plot_accessible_area(ax2, alpha=0.5)
        lidar_obj.plot_score(ax2)
        lidar_obj.plot_wave(ax3)

        canvas_draw(canvas, canvas2, canvas3)
        return lidar_obj


def just_go(start, destination, radius, save=False, vmap_obj=None, file=None, ax=None, ax3=None, fig=None, savename=None, folder_name=None, rtn_step=False, num=150):
    Controller = lidar_Controller()

    if(vmap_obj != None):
        robot = lidar(start, destination, radius, input_map=vmap_obj)
    else:
        robot = lidar(start, destination, radius, filename=file)

    end_type = "None"

    while(not robot.if_in_dest()):
        if(robot.run_times_equalmore_than(num)):
            print("Time Out!")
            end_type = "time_out"
            break
        else:
            Controller.run(robot)

    if(end_type != "time_out"):
        end_type = "done"

    if(ax != None):
        robot.plot_his(ax)
    if(ax3 != None):
        robot.plot_wave(ax3)

    dis = robot.getter_single("distance")
    print(f"dis={dis}\n")

    if(save and fig != None):
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            script_dir = os.path.dirname(sys.executable)
        else:
            # Running as a script
            script_dir = os.path.dirname(os.path.abspath(__file__))

        if(end_type == "done"):
            fig.savefig(
                f"{script_dir}\\test_result\\{folder_name}\\success\\{savename}.png")
            if(rtn_step):
                return (True, robot.getter_single("step"))
        else:
            fig.savefig(
                f"{script_dir}\\test_result\\{folder_name}\\fail\\{savename}.png")
            if(rtn_step):
                return (False, robot.getter_single("step"))

    return True


# -------------------------------------------------
def plot_the_final(ax, lidar_obj: lidar, end_type: str):
    '''
    time_out or done
    '''
    curr = lidar_obj.getter_single("cp")
    lidar_obj.plot_scan_range(ax)

    if(end_type == "done"):

        ax.text(curr[0], curr[1], "Done!",
                ha='right', va='bottom', fontsize=8, color='purple', fontstyle='italic')
    elif(end_type == "time_out"):

        ax.text(curr[0], curr[1], "Time Out!",
                ha='right', va='bottom', fontsize=8, color='purple', fontstyle='italic')


def clear_canvas(ax, ax2, ax3):
    ax.clear()
    ax2.clear()
    ax3.clear()


def canvas_draw(canvas, canvas2, canvas3):
    canvas.draw()
    canvas2.draw()
    canvas3.draw()
    canvas.flush_events()
    canvas2.flush_events()
    canvas3.flush_events()


if __name__ == "__main__":
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot()

    just_go([9.30910782489472, 9.830842355426457], [
            13.590608167662328, 8.576023237391073], 1, save=True, file="777.txt", ax=ax, fig=fig, savename='test')
