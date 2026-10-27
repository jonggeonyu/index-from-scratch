from tools import make_data

table = []

def insert(table, rec):
    table.append(rec)

def select_eq(table, key):
    for rec in table:
        if rec[0] == key:
            return rec
    return None

def select_range(table, low, high):
    lst = []
    for rec in table:
        if low <= rec[0] < high:
            lst.append(rec)
    return lst
