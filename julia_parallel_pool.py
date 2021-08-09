from multiprocessing import Pool
import time
import numpy as np
import matplotlib.pyplot as plt
import os

def julia(comp):
    max = 200
    re, im = comp[0], comp[1]
    #実部が-0.7、虚部が-0.3の複素数cを作成(ここの数値を変えればさまざまなジュリア集合を作れる)
    c = complex(-0.7, -0.3)

    #実部がre、虚部がimの複素数zを作成
    z = complex(re, im)

    for i in range(max):
        z = z*z + c
        #zの絶対値が一度でも2を超えればzが発散することを利用
        if abs(z) >= 2:
            return i        #発散する場合には何回目のループで終わったかを返す
    
    return max  #無限大に発散しない場合にはmaxを返す
    
def main():
    pic_size = 1000
    re = np.linspace(-2, 2, pic_size)
    im = np.linspace(2, -2, pic_size)
    
    #実部と虚部の組み合わせを作成
    Re, Im = np.meshgrid(re, im)
    comp = np.c_[Re.ravel(), Im.ravel()]

    #計算結果を格納するための零行列を作成
    Julia = np.zeros(len(comp))

    start = time.time()
    with Pool(processes=4) as p:
        result = p.map(func=julia, iterable=comp)
    print ("実行時間: ", time.time() - start, "sec")
    
    for i in range(len(result)):
        Julia[i] = result[i]
    Julia = Julia.reshape((pic_size, pic_size))
    fix = plt.figure(dpi=100)
    plt.imshow(Julia, cmap="bone", extent=[-2, 2, -2, 2])
    plt.show()


if __name__ == "__main__":
    main()