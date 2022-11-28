import re
from typing import Union

import fastapi
from fastapi import FastAPI, HTTPException, Response


import Truths

app = FastAPI()


# @app.get("/convert")
# def convert_base(num: Union[int, str], to_base=10, from_base=10):
#    # first convert to decimal number
#    n = int(num, from_base) if isinstance(num, str) else num
#    # now convert decimal to 'to_base' base
#    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#    res = ""
#    while n > 0:
#        n, m = divmod(n, to_base)
#        res += alphabet[m]
#    return res[::-1]


@app.get("/from_dec")
def from_dec(num: int, to_base: int, response: Response):
    response.headers["Cache-Control"] = "max-age=31536000, immutable"
    if to_base > 36: raise HTTPException(403, "Слишком большая система счисления")
    from_dec.t = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    r = ''
    steps = []
    while num:
        steps.append(str(num) + ":" + str(to_base) + " ост: " + str(divmod(num, to_base)[1]))
        num, y = divmod(num, to_base)
        r = from_dec.t[y] + r
    return {"result": r, "steps": steps}


@app.get("/to_dec")
def to_dec(num: str, from_base: int, response: Response):
    response.headers["Cache-Control"] = "max-age=31536000, immutable"
    if from_base > 36: raise HTTPException(403, "Слишком большая система счисления")
    to_dec.t = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    n = num
    res = 0
    steps = []
    summa = []
    # computing max power value
    size = len(n) - 1
    for num in n:
        if to_dec.t.index(num) >= from_base: raise HTTPException(403, "Недопустимое значение")
        steps.append(f"{to_dec.t.index(num)} * {from_base}^{size} = {to_dec.t.index(num) * from_base ** size}")
        res = res + to_dec.t.index(num) * from_base ** size
        summa.append(str(to_dec.t.index(num) * from_base ** size))
        size = size - 1
    steps.append(f"{' + '.join(summa)} = {res}")
    return {"result": res, "steps": steps}


@app.get("/sum")
def sum(num1: str, num2: str, base1: int, base2: int, response: Response):
    response.headers["Cache-Control"] = "max-age=31536000, immutable"
    steps = []
    steps.append("Переводим первое число в десятичную систему")
    if base1 != 10:
        res = to_dec(num1, base1)
        num1 = res.get("result")
        steps += res.get("steps")
    steps.append("Переводим второе число в десятичную систему")
    if base2 != 10:
        res2 = to_dec(num2, base2)
        num2 = res2.get("result")
        steps += res2.get("steps")
    steps.append("Складываем полученные результаты")
    return num1 + num2, steps


@app.get("/multiplication")
def multiplication(num1: str, num2: str, base1: int, base2: int, response: Response):
    response.headers["Cache-Control"] = "max-age=31536000, immutable"
    steps = []
    steps.append("Переводим первое число в десятичную систему")
    if base1 != 10:
        res = to_dec(num1, base1)
        num1 = res.get("result")
        steps += res.get("steps")
    steps.append("Переводим второе число в десятичную систему")
    if base2 != 10:
        res2 = to_dec(num2, base2)
        num2 = res2.get("result")
        steps += res2.get("steps")
    steps.append("Умножаем полученные результаты")
    return num1 * num2, steps


@app.get("/division")
def division(num1: str, num2: str, base1: int, base2: int, response: Response):
    response.headers["Cache-Control"] = "max-age=31536000, immutable"
    steps = []
    steps.append("Переводим первое число в десятичную систему")
    if base1 != 10:
        res = to_dec(num1, base1)
        num1 = res.get("result")
        steps += res.get("steps")
    steps.append("Переводим второе число в десятичную систему")
    if base2 != 10:
        res2 = to_dec(num2, base2)
        num2 = res2.get("result")
        steps += res2.get("steps")
    steps.append("Делим полученные результаты")
    return num1 / num2, steps


@app.get("/subtraction")
def subtraction(num1: str, num2: str, base1: int, base2: int, response: Response):
    response.headers["Cache-Control"] = "max-age=31536000, immutable"
    steps = []
    steps.append("Переводим первое число в десятичную систему")
    if base1 != 10:
        res = to_dec(num1, base1)
        num1 = res.get("result")
        steps += res.get("steps")
    steps.append("Переводим второе число в десятичную систему")
    if base2 != 10:
        res2 = to_dec(num2, base2)
        num2 = res2.get("result")
        steps += res2.get("steps")
    steps.append("Вычитаем полученные результаты")
    return num1 - num2, steps


@app.get("/truth")
def truth_table(funcs: str, response: Response):
    response.headers["Cache-Control"] = "max-age=31536000, immutable"
    variables = sorted(set(re.findall(r"[A-Za-z]", funcs)))
    try:
        data = Truths.Truths(list(variables), [funcs]).to_list()
        return {"data": data}
    except Exception:
        return "Неверный ввод"
