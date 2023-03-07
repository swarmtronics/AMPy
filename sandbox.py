from multiprocessing.pool import Pool
import os
from time import time

def f(x):
    return x**2


def main():
    data = [i for i in range(100000000)]
    with Pool(os.cpu_count()) as pool:
        t1 = time()
        #result = [f(x) for x in data]
        result = pool.map(f, data, chunksize=100000000 //16)
        print(time() - t1)



if __name__ == '__main__':
    main()