import random
import time


def timer_log(func):
    """记录时间的日志装饰器"""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"函数{func.__name__}耗时{(end_time - start_time):.2f}秒")
        return result

    return wrapper


@timer_log
def demo_func():
    """模拟的函数"""
    # 模拟操作耗时1-3秒
    time.sleep(random.randint(1, 3))
    print("模拟的函数执行了")


if __name__ == '__main__':
    demo_func()
