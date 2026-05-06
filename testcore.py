import numpy as np
import multiprocessing
import time

def numpy_stress(process_id, shared_dict):
    size = 2000 
    ops_per_iteration = 2 * (size ** 3)
    
    print(f"进程 {process_id} 启动 | 矩阵大小: {size}x{size}")
    
    while True:
        start_time = time.perf_counter()
        
        # 执行核心计算
        a = np.random.rand(size, size).astype(np.float64)
        b = np.random.rand(size, size).astype(np.float64)
        np.dot(a, b)
        
        end_time = time.perf_counter()
        duration = end_time - start_time
        
        gflops = (ops_per_iteration / duration) / 1e9
        
        # 将结果存入共享字典供主进程汇总
        shared_dict[process_id] = gflops

if __name__ == "__main__":
    cores = multiprocessing.cpu_count()
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()
    
    print(f"系统检测到 {cores} 个核心，开始性能测试...")
    
    pool = []
    for i in range(cores):
        p = multiprocessing.Process(target=numpy_stress, args=(i, shared_dict))
        p.daemon = True 
        p.start()
        pool.append(p)

    try:
        print(f"{'时间(s)':<10} | {'总算力 (GFLOPS)':<20} | {'每核心平均 (GFLOPS)':<20}")
        print("-" * 60)
        start_test = time.time()
        
        while True:
            time.sleep(2) 
            if len(shared_dict) > 0:
                values = list(shared_dict.values())
                total_gflops = sum(values)
                avg_gflops = total_gflops / len(values)
                elapsed = int(time.time() - start_test)
                
                print(f"{elapsed:<10} | {total_gflops:<20.2f} | {avg_gflops:<20.2f}")
                
    except KeyboardInterrupt:
        print("\n测试停止，正在关闭进程...")
        for p in pool:
            p.terminate()