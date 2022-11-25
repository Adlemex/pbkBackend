from typing import Union

import fastapi
from fastapi import FastAPI

app = FastAPI()


#@app.get("/convert")
#def convert_base(num: Union[int, str], to_base=10, from_base=10):
#    # first convert to decimal number
#    n = int(num, from_base) if isinstance(num, str) else num
#    # now convert decimal to 'to_base' base
#    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#    res = ""
#    while n > 0:
#        n, m = divmod(n, to_base)
#        res += alphabet[m]
#    return res[::-1]



@app.get("/from_10")
def from_10(sys: int, num: int):
    from_10.t = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    r = ''
    steps = ""
    while num:
        steps += str(num) + ":" + str(sys) + " ост: " + str(divmod(num, sys)[1]) + "; "
        num, y = divmod(num, sys)
        r = from_10.t[y] + r
    return r, steps


@app.get("/to_10")
def bin_dec(num: str, from_base: int):
    table = {'0': 0, '1': 1, '2': 2, '3': 3,
             '4': 4, '5': 5, '6': 6, '7': 7,
             '8': 8, '9': 9, 'A': 10, 'B': 11,
             'C': 12, 'D': 13, 'E': 14, 'F': 15}

    hexadecimal = num
    res = 0
    steps = ""
    # computing max power value
    size = len(hexadecimal) - 1

    for num in hexadecimal:
        steps += f"{table[num]} * {from_base}^{size} = {table[num] * from_base ** size}; "
        res = res + table[num] * from_base ** size
        size = size - 1
    return res, steps
