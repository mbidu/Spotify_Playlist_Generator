import time
import multiprocessing
from multiprocessing import freeze_support
import numpy as np

def train(l):
    l_fact = list(range(l))
    i_fact = list(range(l))
    # rank = multiprocessing.current_process().name one can also use
    # rank = multiprocessing.current_process()._identity[0]
    # print(f'I am processor {rank}, got n={n}, and finished calculating the factorial.')
    return l_fact, i_fact

if __name__ == '__main__':
    freeze_support()
    start_time = time.time()
    cpu_count = multiprocessing.cpu_count()
    input_params_list = range(1, cpu_count+1)
    print(input_params_list)

    l = list(range(15))
    pool = multiprocessing.Pool(cpu_count)
    d_sums_i, d_counts_i = zip(*pool.map(train, l))
    print(d_sums_i)
    pool.close()
    pool.join()
    # for item in l_fact_new:
    #     dic |= item
    # print(dic)
    # print("--- Multiprocessing: %s seconds ---" % (time.time() - start_time))
    # start_time = time.time()

    # dic = {}
    # for i in range(1, cpu_count+1):
    #     l_fact_new = worker(i)
    #     dic |= l_fact_new
    # print(dic)
    # print("--- Standard: %s seconds ---" % (time.time() - start_time))