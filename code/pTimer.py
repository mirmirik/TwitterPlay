from time import time
from functools import wraps
import random

def timeit(func):
    """
    :param func: Decorated function
    :return: Execution time for the decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f'{func.__name__} executed in {end - start:.4f} seconds')
        return result

    return wrapper


# An arbitrary function
@timeit
def sort_rnd_num():
    numbers = [random.randint(100, 200) for _ in range(100000)]
    numbers.sort()
    return numbers