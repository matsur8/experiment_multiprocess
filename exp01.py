import multiprocessing
import numpy as np
import time, os
import queue

def f(q_e, q_p):
    exq = queue.Queue()
    n_param = 0
    param =(np.random.normal(size=(1,2)), 0)
    #print(q_p.maxsize)
    for i in range(3):
        q_p.put(param)
    for i in range(30):
        print('before get ex', n_param, q_e.empty())
        #while True:
        #    try:
        ex, req_p = q_e.get()
        #    except queue.Empty:
        #        break
        if req_p:
            n_param += 1
            print('before put param', n_param, q_p.qsize())
            q_p.put(param)
        #except queue.Empty:
        #  
        print('aft')
        
        time.sleep(0.3 * np.random.random() + 0.3)
        param =(np.random.normal(size=(1,2)), i+1)
        #print('end')
    for i in range(3):
        q_p.put(None)
    print('end f', n_param)

def g(q_e, q_p):
    param = q_p.get()
    n_empty = 0
    n_req = 0
    n_try = 0
    not_got = False
    for i in range(100):
        time.sleep(np.random.random() + 1)
        get_param_this_time = True #np.random.random() > 0.5
        if get_param_this_time and not not_got:
            n_req += 1
        print('act', os.getpid(), i, get_param_this_time and not not_got)
        q_e.put([('act', os.getpid(), i), get_param_this_time and not not_got])
        if not_got or get_param_this_time:
            n_try += 1
            not_got = False
            try:
                param = q_p.get(True, 100)
                print(os.getpid(), param)
            except queue.Empty:
                n_empty += 1
                not_got = True
                print('empty', os.getpid(), param)
        print('ei', os.getpid(), n_req, n_try, n_empty)
        if param is None:
            print('exit with param is None', os.getpid())
            break
    print('exit g', os.getpid(), n_req, n_try, n_empty)
        

if __name__ == '__main__':
    y = 2
    x = 4
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
    queue_experience = multiprocessing.Queue()
    queue_params = multiprocessing.Queue(5)
    ps = [multiprocessing.Process(target=f, args=(queue_experience, queue_params))]
    for i in range(3):
        ps.append(multiprocessing.Process(target=g, args=(queue_experience, queue_params)))
    for p in ps:
        p.start()
    for p in ps:
        p.join()