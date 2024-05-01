import random
from numpy import zeros as npzeros
from numpy import sum as npsum
import matplotlib.pyplot as plt
import os
import re
import threading
import multiprocessing
import queue
import sys
#------------------------
from main import just_go

class area:
    def __init__(self,lb:list,ru:list) -> None:
        self.lb=lb
        self.ru=ru

    def generate_random_point(self, num):
        self.points = npzeros((num, 2))
        for i in range(num):
            x = random.uniform(self.lb[0]+0.001, self.ru[0]-0.001)
            y = random.uniform(self.lb[1]+0.001, self.ru[1]-0.001)
            self.points[i] = (x, y)

    def random_one_point(self):
        x = random.uniform(self.lb[0]+0.001, self.ru[0])
        y = random.uniform(self.lb[1]+0.001, self.ru[1])
        return (x, y)       
    
    def __len__(self):
        return len(self.points)

def worker(i,k, ax,fig,start, end, radius, filename,filename_pure,queue,time_out_num):
    result=just_go(start, end, radius,save=True,ax=ax,file=filename,fig=fig,savename=str(i),folder_name=filename_pure,rtn_step=True,num=time_out_num)
    ax.clear()
    queue.put((k,result[0],result[1]))

def test_and_save(area_list:list,radius,file_name,num,max):
    count=int(num/8)
    file_name_pure=file_name[:-4]
    step_list=[]

    for item in area_list:
        item.generate_random_point(count)


    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        script_dir = os.path.dirname(sys.executable)
    else:
        # Running as a script
        script_dir = os.path.dirname(os.path.abspath(__file__))

    folder_path_succ = os.path.join(script_dir, f'test_result\\{file_name_pure}\\success')
    folder_path_fail = os.path.join(script_dir, f'test_result\\{file_name_pure}\\fail')
    folder_path_result = os.path.join(script_dir, f'test_result\\{file_name_pure}')

    if not os.path.exists(folder_path_succ):
        os.makedirs(folder_path_succ)
    if not os.path.exists(folder_path_fail):
        os.makedirs(folder_path_fail)

    axs=[]
    figs=[]
    for j in range(10):
        fig1 = plt.figure(figsize=(6, 6))
        ax1 = fig1.add_subplot()
        figs.append(fig1)
        axs.append(ax1)

    
    test=((0,1),(1,0),(2,3),(3,2),(4,5),(5,4),(6,7),(7,6))
    step_list = npzeros((num,))

    
    i=0
    success=0
    while(i<num):
        setting=test[int(i/count)]
        

        a=area_list[setting[0]]
        b=area_list[setting[1]]
             
        result_queue = queue.Queue()

        ths=[]

        for j in range(10):
            start=a.random_one_point()
            end=b.random_one_point()
            t1 = threading.Thread(target=worker, args=(i+j, j+1,axs[j],figs[j],start, end, radius,file_name,file_name_pure,result_queue,max))
            ths.append(t1)

        for item in ths:
            item.start()

        for yyy in range(10):
            k,s,steps_count = result_queue.get()
            if(s):
                success+=1
            step_list[k-1+i]=steps_count

        for item in ths:
            item.join()
       
        i+=10

    ax1.clear()
    ax1.plot(range(0,num),step_list,color="orange")

    data = [x for x in step_list if x < 150]
    total_step=npsum(data)
    ax1.plot([0,num],[total_step/len(data),total_step/len(data)],color="blue")
    
    ax1.text(0.9, 0.9, f"success_rate:{success/num}", transform=ax1.transAxes, ha='right', va='top', bbox=dict(facecolor='white', edgecolor='red', boxstyle='round'))
    fig1.savefig(f"{folder_path_result}\\summary.png")
    
    return success/num

def test_and_save_random_area(area_list:list,radius,file_name,num,max):
    file_name_pure=file_name[:-4]
    step_list=[]


    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        script_dir = os.path.dirname(sys.executable)
    else:
        # Running as a script
        script_dir = os.path.dirname(os.path.abspath(__file__))

    folder_path_succ = os.path.join(script_dir, f'test_result\\{file_name_pure}\\success')
    folder_path_fail = os.path.join(script_dir, f'test_result\\{file_name_pure}\\fail')
    folder_path_result = os.path.join(script_dir, f'test_result\\{file_name_pure}')

    if not os.path.exists(folder_path_succ):
        os.makedirs(folder_path_succ)
    if not os.path.exists(folder_path_fail):
        os.makedirs(folder_path_fail)
    
    for item in area_list:
        item.generate_random_point(num)


    step_list = npzeros((num,))
    axs=[]
    figs=[]
    for j in range(10):
        fig1 = plt.figure(figsize=(6, 6))
        ax1 = fig1.add_subplot()
        figs.append(fig1)
        axs.append(ax1)
    
    i=0
    success=0
    while(i<num):
             
        result_queue = queue.Queue()

        ths=[]

        for j in range(10):
            a, b = random.sample(area_list, 2)
            start=a.random_one_point()
            end=b.random_one_point()
            t1 = threading.Thread(target=worker, args=(i+j, j+1,axs[j],figs[j],start, end, radius, file_name,file_name_pure,result_queue,max))
            ths.append(t1)

        for item in ths:
            item.start()

        for yyy in range(10):
            k,s,steps_count = result_queue.get()
            if(s):
                success+=1
            step_list[k-1+i]=steps_count

        for item in ths:
            item.join()
       
        i+=10

    ax1.clear()
    ax1.plot(range(0,num),step_list,color="orange")

    data = [x for x in step_list if x < 150]
    total_step=npsum(data)
    ax1.plot([0,num],[total_step/len(data),total_step/len(data)],color="blue")
    
    ax1.text(0.9, 0.9, f"success_rate:{success/num}", transform=ax1.transAxes, ha='right', va='top', bbox=dict(facecolor='white', edgecolor='red', boxstyle='round'))
    fig1.savefig(f"{folder_path_result}\\summary.png")
    
    return success/num

def read(file_name, path_type='relative',random_area=False):
        
        
        if(path_type == 'relative'):
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                script_dir = os.path.dirname(sys.executable)
            else:
                # Running as a script
                script_dir = os.path.dirname(os.path.abspath(__file__))

            path = script_dir+"\\test_sets\\"+file_name

        print(path)

        f = open(path, mode='r', encoding="utf-8")
        if f == None:
            raise IOError
        
        target_name=f.readline()[:-1]
        area_list=[]

        while (1):
            line = f.readline()
            if(line == ""):
                break

            if "radius" in line:
                s = line.replace("radius:", "")
                radius=float(s)

            elif "num" in line:
                s = line.replace("num:", "")
                num=int(s)

            elif "max" in line:
                s = line.replace("max:", "")
                max=int(s)

            elif "(" in line:
                matches = re.findall(r'[-+]?\d*\.\d+|\d+',line)
                for i in range(len(matches)):
                    matches[i]=float(matches[i])

                if(len(matches)==4):
                    temp=area([*matches[:2]],[*matches[2:]])
                    area_list.append(temp)

            else:
                print("read_test_sets_warning")

        f.close()

        if(random_area):
            return test_and_save_random_area(area_list,radius,target_name,num,max)
        else:
            return test_and_save(area_list,radius,target_name,num,max)

if __name__ == "__main__":
    processes = []
    

    files=["test_map_test.txt","test_map_2_test.txt","test_map_3_test.txt"]
    num_processes = len(files)
    i=0

    for i in range(num_processes):
        p = multiprocessing.Process(target=read, args=(files[i],"relative"))
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print('All processes have completed')



            