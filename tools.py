import random
import time

def make_data(n):
    lst = []
    for i in range(n):
        rec = (i, "user" + str(i))
        lst.append(rec)
    return lst