import timeit
import numpy as np
import random


mask = np.array([
        [0,0,0,1,0,0,0],
        [0,0,1,1,1,0,0],
        [0,0,0,1,0,0,0],
    ]).astype(bool)


big = np.zeros((100000,7)).astype(bool);

small = np.zeros((100,7)).astype(bool);

def bigRandOr():
    y = random.randint(4,len(big)-4);
    result = mask | big[y:y+3]

def smallRandOr():
    y = random.randint(4,len(small)-4);
    result = mask | small[y:y+3];

bigTime = timeit.timeit('bigRandOr()', number=100000, globals=globals())
smallTime = timeit.timeit('smallRandOr()', number=100000, globals=globals())

print(bigTime,smallTime);
