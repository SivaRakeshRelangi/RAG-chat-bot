import time

def measure_latency(func, *args):
    start = time.time()
    result = func(*args)
    return result, time.time() - start