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

def julia_b(list,r_dict,p_num):
    julia_list = []
    for i, c_point in enumerate(list):
        julia_list.append(julia(200, c_point))
    r_dict[p_num] = julia_list


def main():
    pic_size = 1000
    re = np.linspace(-2, 2, pic_size)
    im = np.linspace(2, -2, pic_size)

    Re, Im = np.meshgrid(re, im)
    comp = np.c_[Re.ravel(), Im.ravel()]

    slice = 8
    test = len(comp)//slice
    slice_list = []
    for y in range(slice):
        slice_list.append(comp[test*y:test*(y+1)])

    J = []
    process_list = []
    result_list = [0]*slice
    manager = Manager()
    return_dict = manager.dict()

    start = time.time()
    for p in range(slice):
        process = Process(target=julia_b,kwargs={'list':slice_list[p],'r_dict':return_dict,'p_num':p})
        process_list.append(process)
        process.start()
    
    for j in process_list:
        j.join()
    
    for n in range(slice):
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