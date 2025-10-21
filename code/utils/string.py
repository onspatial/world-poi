import time
def print_time(*args, **kwargs):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{current_time}]: ", *args, **kwargs)