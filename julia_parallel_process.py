from multiprocessing import Process,Manager
import numpy as np
import time
import matplotlib.pyplot as plt
import os

def julia(max, comp):
    re, im = comp[0], comp[1]
    c = complex(-0.7, -0.3)
    z = complex(re, im)

    for i in range(max):
        z = z*z + c
        if abs(z) >= 2:
            return i
    
    return max

def bet_julia(list,r_dict,p_num):
    # print("julia_start. {}".format(os.getpid()))
    julia_list = []
    for i, c_point in enumerate(list):
        julia_list.append(julia(200, c_point))
    # print("julia_end. {}".format(os.getpid()))
    r_dict[p_num] = julia_list


def main():
    pic_size = 1000
    # print("start. {}".format(os.getpid()))
    re = np.linspace(-2, 2, pic_size)
    im = np.linspace(2, -2, pic_size)

    Re, Im = np.meshgrid(re, im)
    comp = np.c_[Re.ravel(), Im.ravel()]

    slicenum = 8
    testt = len(comp)//slicenum
    slice_list = []
    for y in range(slicenum):
        slice_list.append(comp[testt*y:testt*(y+1)])

    J = []
    process_list = []
    result_list = [0]*slicenum
    manager = Manager()
    return_dict = manager.dict()


    start = time.time()
    for p in range(slicenum):
        process = Process(target=bet_julia,kwargs={'list':slice_list[p],'r_dict':return_dict,'p_num':p})
        process_list.append(process)
        process.start()
    
    for j in process_list:
        j.join()
    
    for n in range(slicenum):
        result_list[n] = return_dict[n]
    
    for i in result_list:
        J.extend(i)

    print ("実行時間: ", time.time() - start, "sec")

    Julia = np.array(J)
    Julia = Julia.reshape((pic_size, pic_size))
    fix = plt.figure(dpi=100)
    plt.imshow(Julia, cmap="bone", extent=[-2, 2, -2, 2])
    plt.show()

    

    

if __name__ == "__main__":
    main()