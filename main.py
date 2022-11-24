import fastapi
from fastapi import FastAPI

app = FastAPI()


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
