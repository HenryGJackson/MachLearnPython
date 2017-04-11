import pandas as pd
import numpy as np

a = [[0] for i in range(0,10)]
b = [[0] for i in range(0,5)]
c = []

for i in range(0,10):
    a[i] = i
    if(i<5):
        b[i] = 10-i

c.append(a)
c.append(b)
print c
