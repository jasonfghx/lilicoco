import ctypes
import sys
import re
from os import getcwd, path

import matplotlib
from matplotlib import patches
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

import platform
#-----------------------#
from vector_map import Vector_map
from lidar import lidar
from decision_tree import lidar_Controller
import main

#------- color ----------------#
window_bg = '#212121'
window_fg = '#bdbdbd'
item_bg = '#3b3b3b'
item_acti_bg = '#787878'
item_highlight = "#4CAF50"
item_err = '#E63946'
#-------- size ----------------#
length = 1500
height = 900
#-------- font ----------------#
item_font = ("TkDefaultFont", 12)
#------------------------------#
# ctypes.windll.shcore.SetProcessDpiAwareness(1)
#------------------------------#
curr_entry = None
global_canvas = None
global_vvv = None
global_ax = None
#------------------------------#


class UI():

    def __init__(self, window, frame_left, frame_right, frame_bottom, top):
        matplotlib.use("TkAgg")
        self.fig = plt.figure()
        self.fig2 = plt.figure()
        self.fig3 = plt.figure(figsize=(12, 1))

        self.ax = self.fig.add_subplot()
        self.ax2 = self.fig2.add_subplot()
        self.ax3 = self.fig3.add_subplot()

        self.fig.tight_layout()
        self.fig2.tight_layout()
        self.fig3.tight_layout()

        global global_ax
        global_ax = self.ax

        self.mainwindow = window
        self.master1 = frame_left
        self.master2 = frame_right
        self.master3 = frame_bottom
        self.top = top

        self.next_step = tk.BooleanVar(value=False)
        self.selection = tk.IntVar()

        # entry_radius and entry_precision default
        self.radius_default = tk.StringVar(value='1')

        self.vvv = None

        self.canvas = None
        self.canvas2 = None
        self.canvas3 = None

        self.draw_para = tuple(
            (self.ax, self.ax2, self.ax3, self.canvas, self.canvas2, self.canvas3))

        self.set_botton()
        self.set_label()
        self.set_entry()
        self.set_radio()
        self.set_text()
        self.set_stdio()

    def set_botton(self):
        # botton of import
        self.bt_import_map = tk.Button(self.master1, text='import map', width='15', command=lambda: self.import_map(),
                                       bg=item_bg, fg=window_fg, font=item_font,
                                       activebackground=item_acti_bg, activeforeground=window_fg)
        self.bt_import_map.place(x='20', y='10')

        # bottom of go
        self.bt_go = tk.Button(self.master1, text='go', width='15', height='1', command=lambda: self.go(),
                               bg=item_bg, fg=window_fg, font=item_font,
                               activebackground=item_acti_bg, activeforeground=window_fg)
        self.bt_go.place(x='600', y='65')
        self.bt_go.config(state="disabled")

        # bottom of next
        self.bt_next = tk.Button(self.master1, text='continue', width='15', height='1', command=lambda: self.next_step.set(value=True),
                                 bg=item_bg, fg=window_fg, font=item_font,
                                 activebackground=item_acti_bg, activeforeground=window_fg)
        self.bt_next.place(x='600', y='95')
        self.bt_next.config(state="disabled")

        # botton of clear
        self.bt_clear = tk.Button(self.master2, text='clear', width='15', command=lambda: self.clear(),
                                  bg=item_bg, fg=window_fg, font=item_font,
                                  activebackground=item_acti_bg, activeforeground=window_fg)
        self.bt_clear.place(x='60', y='10')
        self.bt_clear.config(state="disabled")

    def set_label(self):
        # label of file name
        self.lb_input = tk.Label(self.master1, anchor='nw', text='input :  NONE',
                                 bg=window_bg, fg=window_fg, font=("TkDefaultFont", 10))
        self.lb_input.place(anchor='nw', x='200', y='10')

        # label of start
        self.lb_start = tk.Label(self.master1, anchor='center', text='start',
                                 width='15', bg=window_bg, fg=window_fg, font=item_font)
        self.lb_start.place(anchor='nw', x='20', y='40')

        # label of dest
        self.lb_dest = tk.Label(self.master1, anchor='center', text='destination',
                                width='15', bg=window_bg, fg=window_fg, font=item_font)
        self.lb_dest.place(anchor='nw', x='200', y='40')

        # label of radius
        self.lb_r = tk.Label(self.master1, anchor='nw', text='radius',
                             width='15', bg=window_bg, fg=window_fg, font=item_font)
        self.lb_r.place(anchor='nw', x='400', y='40')

    def set_entry(self):
        self.entry_start = tk.Entry(self.master1,  bg=window_bg,
                                    fg=window_fg, bd=0, insertbackground=window_fg, font=("Arial", 10))
        self.entry_start.place(x=20, y=60, width=160, height=30)
        self.entry_start.bind(
            "<FocusIn>", lambda event: self.set_focus(self.entry_start))

        self.entry_dest = tk.Entry(self.master1,  bg=window_bg,
                                   fg=window_fg, bd=0, insertbackground=window_fg, font=("Arial", 10))
        self.entry_dest.place(x=200, y=60, width=160, height=30)
        self.entry_dest.bind(
            "<FocusIn>", lambda event: self.set_focus(self.entry_dest))

        self.entry_radius = tk.Entry(self.master1,  bg=window_bg,
                                     fg=window_fg, bd=0, insertbackground=window_fg, font=("Arial", 10),
                                     textvariable=self.radius_default)
        self.entry_radius.place(x=400, y=60, width=80, height=30)

    def set_radio(self):

        # thru
        self.radio_thru = tk.Radiobutton(self.master1, text="thru",
                                         variable=self.selection, value=1, bg=window_bg,
                                         fg=window_fg, activebackground=item_acti_bg, activeforeground=window_bg,
                                         selectcolor=window_bg, font=(
                                             "Arial", 10))
        self.radio_thru.place(x=20, y=90, width=60, height=30)

        # step
        self.radio_step = tk.Radiobutton(self.master1, text="step by step",
                                         variable=self.selection, value=2, bg=window_bg,
                                         fg=window_fg, activebackground=item_acti_bg, activeforeground=window_bg,
                                         selectcolor=window_bg, font=(
                                             "Arial", 10))
        self.radio_step.place(x=200, y=90, width=100, height=30)

        # step
        self.radio_just_go = tk.Radiobutton(self.master1, text="just go",
                                            variable=self.selection, value=3, bg=window_bg,
                                            fg=window_fg, activebackground=item_acti_bg, activeforeground=window_bg,
                                            selectcolor=window_bg, font=(
                                                "Arial", 10))
        self.radio_just_go.place(x=380, y=90, width=100, height=30)

        self.radio_thru.select()

    def set_text(self):
        self.text_output = tk.Text(self.top, bg=window_bg, fg=window_fg)
        self.text_output.tag_config(
            'tag_red', foreground=item_err, font=("TkDefaultFont", 12))
        self.text_output.tag_config(
            'tag_norm', foreground=window_fg, font=("TkDefaultFont", 12))
        self.text_output.pack(fill="both", expand=True)

    def set_stdio(self):
        my_stdout = Guistdout(self.mainwindow, self.text_output)
        my_stderr = Guisterr(self.mainwindow, self.text_output)

        sys.stdout = my_stdout
        sys.stderr = my_stderr

    def import_map(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            messagebox.showinfo("Info", "Import failed")
        else:
            self.text_output.delete("1.0", "end")
            path_list = file_path.split('/')
            determine_path_list = file_path.split('.')

            if(determine_path_list[len(determine_path_list)-1] != 'txt'):
                messagebox.showinfo("Info", "Wrong format!")
                return

            if(self.canvas == None and self.canvas2 == None):
                self.canvas = FigureCanvasTkAgg(
                    figure=self.fig, master=self.master1)
                self.canvas2 = FigureCanvasTkAgg(
                    figure=self.fig2, master=self.master2)
                self.canvas3 = FigureCanvasTkAgg(
                    figure=self.fig3, master=self.master3)
                self.canvas.get_tk_widget().place(x='40', y='150', width='600', height='600')
                self.canvas2.get_tk_widget().place(x='40', y='150', width='600', height='600')
                self.canvas3.get_tk_widget().place(x='2', y='2', width='1500', height='150')
                self.draw_para = tuple(
                    (self.ax, self.ax2, self.ax3, self.canvas, self.canvas2, self.canvas3))

            else:
                main.clear_canvas(*self.draw_para[:3])

            path = path_list[len(path_list)-3]+'\\'+path_list[len(path_list)-2] + \
                '\\'+path_list[len(path_list)-1]
            self.lb_input.configure(text='path => '+path, fg='white')

            self.vvv = Vector_map()

            self.vvv .readfile(file_path, 'absolute')

            main.clear_canvas(*self.draw_para[:3])
            self.vvv.plot_map(self.ax)

            main.canvas_draw(*self.draw_para[3:])
            self.mouse_event = self.canvas.mpl_connect(
                'button_press_event', onclick)

            global global_canvas
            global global_vvv

            global_canvas = self.canvas
            global_vvv = self.vvv

            self.bt_go.config(state='normal')
            self.bt_go.config(text='go', background=item_bg, foreground=window_fg,
                              activebackground=item_acti_bg, activeforeground=window_fg)
            self.bt_next.config(state='normal')
            self.bt_next.config(text='Next', background=item_bg)

    def go(self):
        if(self.vvv == None):
            print("No map!\n")
            return
        plt.ion()
        self.bt_clear.config(state="disabled")
        self.bt_import_map.config(state="disabled")
        self.bt_go.config(state='disabled')

        startpoint = self.entry_start.get()
        destpoint = self.entry_dest.get()

        radius = self.entry_radius.get()

        try:
            radius = float(radius)
        except:
            print("wrong input r\n")
            self.bt_go.config(state='normal')
            return

        startpoint = [float(s) for s in re.findall(r'-?\d+\.?\d*', startpoint)]
        destpoint = [float(s) for s in re.findall(r'-?\d+\.?\d*', destpoint)]

        lidar_para = tuple((startpoint, destpoint, radius))

        if(len(startpoint) != 2 or len(destpoint) != 2):
            print("wrong input points!\n")
            self.bt_go.config(state='normal')
            return

        size = self.vvv.get_size()

        if(not (inborder(startpoint, size) and inborder(destpoint, size))):
            print("out of border!\n")
            self.bt_go.config(state='normal')
            return

        self.draw_para[-2].mpl_disconnect(self.mouse_event)

        control = lidar_Controller()
        ty = self.selection.get()

        if(ty == 2):
            Robot = lidar(startpoint, destpoint, radius, input_map=self.vvv)
            while(1):
                self.mainwindow.after(
                    10, self.mainwindow.wait_variable(self.next_step))

                self.bt_next.config(state='disabled')

                Robot = main.go_step_by_step(
                    Robot, control, *self.draw_para)
                self.bt_next.config(state='normal')
                self.next_step.set(False)

                if(Robot == "done"):
                    print(Robot.getter_single("distance"))
                    done = True
                    break
                elif(Robot == "time_out"):
                    print(Robot.getter_single("distance"))
                    done = False
                    break
        elif(ty == 1):
            done = main.go_thru(self.vvv, *lidar_para,
                                *self.draw_para)

        else:
            done = main.just_go(
                *lidar_para, vmap_obj=self.vvv, ax=self.ax, ax3=self.ax3)

        if(done != False):
            self.bt_go.config(text='Done!', background=item_highlight)
            self.bt_go.config(state='disabled')
            self.bt_next.config(state='disabled')
        else:
            self.bt_go.config(text='NONE!', background=item_err,
                              foreground='black')
            self.bt_go.config(state='disabled')
            self.bt_next.config(state='disabled')

        plt.ioff()
        self.bt_clear.config(state="normal")

    def clear(self):
        self.bt_clear.config(state='disabled')
        self.bt_go.config(state='disabled')
        self.bt_next.config(state='disabled')
        self.bt_import_map.config(state='normal')
        self.next_step.set(False)

        del self.vvv

        main.clear_canvas(*self.draw_para[:3])
        main.canvas_draw(*self.draw_para[3:])

        self.vvv = None

    def set_focus(self, widget):
        global curr_entry
        curr_entry = widget


class Guistdout():
    def __init__(self, root, label):
        self.root = root
        self.cache = ""
        self.label = label

    def write(self, message):
        if '\n' in message:
            self.cache += message
            self.flush()
        else:
            self.cache += message

    def flush(self):
        if '\r' in self.cache:
            last_line_start = self.label.index("end-1c linestart")
            last_line_end = self.label.index("end-1c lineend")
            self.label.delete(last_line_start, last_line_end)
        self.label.insert(tk.END, self.cache, 'tag_norm')
        self.label.yview_moveto(1.0)
        self.cache = ''


class Guisterr(Guistdout):
    def flush(self):
        if '\r' in self.cache:
            last_line_start = self.label.index("end-1c linestart")
            last_line_end = self.label.index("end-1c lineend")
            self.label.delete(last_line_start, last_line_end)
        self.label.insert(tk.END, self.cache, 'tag_red')
        self.label.yview_moveto(1.0)
        self.cache = ''


def inborder(check, size):
    x, y = check[0], check[1]
    if(x >= size[0] or y >= size[1] or x <= 0 or y <= 0):
        return False
    else:
        return True


def onclick(event):
    x = event.xdata
    y = event.ydata

    print(f"Click on :{x}   ,{y}")
    set_msp_entey((x, y))

    global mouse
    mouse = x, y


def set_msp_entey(data):
    global curr_entry
    if(curr_entry == None):
        return
    curr_entry.delete(0, tk.END)
    curr_entry.insert(0, f"{data[0]},{data[1]}")
    curr_entry = None

    global_ax.clear()
    global_ax.scatter(data[0], data[1])
    global_vvv.plot_map(global_ax)
    global_canvas.draw()


def check_win_version(mainwindow):
    if platform.system() == 'Windows':
        build = int(platform.win32_ver()[1].split('.')[2])
        if build >= 22000:
            print("This is Windows 11.")

            ctypes.windll.shcore.SetProcessDpiAwareness(1)
            #mainwindow.tk.call('tk', 'scaling', 2)
    else:
        print("This script is designed for Windows only.")

# mainloop


if __name__ == '__main__':
    window = tk.Tk()
    window.title('Lidar Algorithm')
    window.geometry(f'{length}x{height}')
    window.resizable(False, False)
    window.config(background=window_bg)

    # frame
    frame_top = tk.Frame(
        window, width=length, height=height-150, bg=window_bg)
    frame_top.pack(side='top')

    frame_bottom = tk.Frame(
        window, width=length, height=150,  bg=window_bg)
    frame_bottom.pack(side='bottom')

    frame_left = tk.LabelFrame(
        frame_top, width=length/2, height=height-150, text='PATH', bg=window_bg, fg=window_fg)
    frame_left.pack(side='left')

    frame_right = tk.LabelFrame(
        frame_top, width=length/2, height=height-150, text='LIDAR', bg=window_bg, fg=window_fg)
    frame_right.pack(side='right')

    frame_bottom = tk.LabelFrame(
        frame_bottom, width=length, height=150, text='wave', bg=window_bg, fg=window_fg)
    frame_bottom.pack(side='bottom')

    # jump out window
    top = tk.Toplevel()
    top.title("Output Message")
    top.resizable(True, True)

    # UI

    app = UI(window, frame_left, frame_right, frame_bottom, top)

    check_win_version(window)

    # mainloop
    app.mainwindow.mainloop()
