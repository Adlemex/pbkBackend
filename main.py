import re
from typing import Union

import fastapi
from fastapi import FastAPI, HTTPException, Response
from Resp import Resp, Block
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
    ans = Resp()
    r = ''
    ans.blocks.append(Block(title=f"Переводим в {to_base}-ую систему делением с остатком"))
    while num:
        ans.blocks[0].steps.append(str(num) + ":" + str(to_base) + " ост: " + str(divmod(num, to_base)[1]))
        num, y = divmod(num, to_base)
        r = from_dec.t[y] + r
    ans.blocks.append(Block(title="Смотрим остатки сверху вниз"))
    ans.blocks[1].steps.append(r)
    ans.result = r
    return ans


@app.get("/to_dec")
def to_dec(num: str, from_base: int, response: Response, text: str =
           "Перевод в 10-ую систему методом возведения в степень"):
    response.headers["Cache-Control"] = "max-age=31536000, immutable"
    if from_base > 36: raise HTTPException(403, "Слишком большая система счисления")
    to_dec.t = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    n = num
    res = 0
    ans = Resp()
    summa = []
    # computing max power value
    size = len(n) - 1
    ans.blocks.append(Block(title=text))
    for numm in n:
        if to_dec.t.index(numm) >= from_base: raise HTTPException(403, "Недопустимое значение")
        ans.blocks[0].steps.append(f"{to_dec.t.index(numm)} * {from_base}^{size} = {to_dec.t.index(numm) * from_base ** size}")
        res = res + to_dec.t.index(numm) * from_base ** size
        summa.append(str(to_dec.t.index(numm) * from_base ** size))
        size = size - 1
    ans.blocks.append(Block(title="Складывание результата"))
    ans.blocks[1].steps.append(f"{' + '.join(summa)} = {res}")
    ans.result = res
    return ans

@app.get("/calc")
def calc(num1: str, num2: str, base1: int, base2: int, action: str, end_base: int, response: Response):
    response.headers["Cache-Control"] = "max-age=31536000, immutable"
    ans = Resp()
    steps = []
    res = ""
    if base1 != 10:
        ress = to_dec(num1, base1, response, "Переводим первое число в десятичную систему")
        num1 = ress.result
        for blockk in ress.blocks:
            ans.blocks.append(blockk)
    if base2 != 10:
        steps.append("Переводим второе число в десятичную систему")
        res2 = to_dec(num2, base2, response, "Переводим второе число в десятичную систему")
        num2 = res2.result
        for blockk in res2.blocks:
            ans.blocks.append(blockk)
    if action == "sum":
        block = Block(title="Складываем полученные числа")
        block.steps.append(f"{num1} + {num2} = {num1+num2}")
        res = num1 + num2
        ans.blocks.append(block)
    if action == "mul":
        block = Block(title="Умножаем полученные числа")
        block.steps.append(f"{num1} * {num2} = {num1*num2}")
        res = num1 * num2
        ans.blocks.append(block)
    if action == "sub":
        block = Block(title="Вычитаем полученные числа")
        block.steps.append(f"{num1} - {num2} = {num1-num2}")
        res = num1 - num2
        ans.blocks.append(block)
    if action == "div":
        block = Block(title="Делим полученные числа")
        block.steps.append(f"{num1} / {num2} = {num1//num2}")
        res = num1 // num2
        ans.blocks.append(block)
    if end_base != 10:
        ress = from_dec(res, end_base, response)
        for blockk in ress.blocks:
            ans.blocks.append(blockk)
        res = ress.result
    ans.result = res
    return ans

@app.get("/sum")
def sum(num1: str, num2: str, base1: int, base2: int, response: Response):
    response.headers["Cache-Control"] = "max-age=31536000, immutable"
    steps = []
    if base1 != 10:
        steps.append("Переводим первое число в десятичную систему")
        res = to_dec(num1, base1)
        num1 = res.get("result")
        steps += res.get("steps")
    if base2 != 10:
        steps.append("Переводим второе число в десятичную систему")
        res2 = to_dec(num2, base2)
        num2 = res2.get("result")
        steps += res2.get("steps")
    steps.append("Складываем полученные результаты")
    return {"result": num1 + num2, "steps": steps}


@app.get("/multiplication")
def multiplication(num1: str, num2: str, base1: int, base2: int, response: Response):
    response.headers["Cache-Control"] = "max-age=31536000, immutable"
    steps = []
    if base1 != 10:
        steps.append("Переводим первое число в десятичную систему")
        res = to_dec(num1, base1)
        num1 = res.get("result")
        steps += res.get("steps")
    if base2 != 10:
        steps.append("Переводим второе число в десятичную систему")
        res2 = to_dec(num2, base2)
        num2 = res2.get("result")
        steps += res2.get("steps")
    steps.append("Умножаем полученные результаты")
    return {"result": num1 * num2, "steps": steps}


@app.get("/division")
def division(num1: str, num2: str, base1: int, base2: int, response: Response):
    response.headers["Cache-Control"] = "max-age=31536000, immutable"
    steps = []
    if base1 != 10:
        steps.append("Переводим первое число в десятичную систему")
        res = to_dec(num1, base1)
        num1 = res.get("result")
        steps += res.get("steps")
    if base2 != 10:
        steps.append("Переводим второе число в десятичную систему")
        res2 = to_dec(num2, base2)
        num2 = res2.get("result")
        steps += res2.get("steps")
    steps.append("Делим полученные результаты")
    return {"result": num1 / num2, "steps": steps}


@app.get("/subtraction")
def subtraction(num1: str, num2: str, base1: int, base2: int, response: Response):
    response.headers["Cache-Control"] = "max-age=31536000, immutable"
    steps = []
    if base1 != 10:
        steps.append("Переводим первое число в десятичную систему")
        res = to_dec(num1, base1)
        num1 = res.get("result")
        steps += res.get("steps")
    if base2 != 10:
        steps.append("Переводим второе число в десятичную систему")
        res2 = to_dec(num2, base2)
        num2 = res2.get("result")
        steps += res2.get("steps")
    steps.append("Вычитаем полученные результаты")
    return {"result": num1 - num2, "steps": steps}


@app.get("/truth")
def truth_table(funcs: str, response: Response):
    response.headers["Cache-Control"] = "max-age=31536000, immutable"
    variables = sorted(set(re.findall(r"[A-Za-z]", funcs)))
    try:
        data = Truths.Truths(list(variables), [funcs]).to_list()
        print(data)
        return {"data": data}
    except Exception:
        return "Неверный ввод"


@app.get("/ch_bases")
def ch_bases(num: str, from_base: int, to_base: int, response: Response):
    if from_base == 10: return from_dec(int(num), to_base, response)
    if to_base == 10: return to_dec(num, from_base, response)
    ans = Resp()
    dec = to_dec(num, from_base, response)
    for block in dec.blocks:
        ans.blocks.append(block)
    new = from_dec(int(dec.result), to_base, response)
    for block in new.blocks:
        ans.blocks.append(block)
    ans.result = new.result
    return ans
