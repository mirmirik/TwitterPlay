from time import time
from functools import wraps
import random
import pytest

def timeit(func):
    """
    :param func: Decorated function
    :return: Execution time for the decorated function
    TM GIT Test
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


def PrintNumber(a, b):
    result = a + b

    if (result >= 0):
        return "Positive"
    else:
        return "Negative"

@pytest.mark.parametrize('testDataA, testDataB, shouldBe', 
        [(3, 5, "Positive"), 
         (-2, -5, "Negative")])
def test_TwitterDateAsString(testData, shouldBe):
    result = PrintNumber(testDataA, testDataB)
    assert result == shouldBe, "PrintNumber is not working correctly."
