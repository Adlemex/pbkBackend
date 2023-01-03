import re
from typing import Union
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, Response
from Resp import Resp, Block
import Truths
import requests

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
    ans.blocks.append(Block(title="Сложение результата"))
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
    try:
        num1 = int(num1)
        num2 = int(num2)
    except ValueError:
        raise HTTPException(403, "Введеные значения не числа")
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

@app.get("/karnaugh_map")
def karnaugh_map(funcs: str, response: Response):
    response.headers["Cache-Control"] = "max-age=31536000, immutable"
    replacement = {"∧": 3, "∨": 4, "->": 5, "⇔": 6, "⊕": 7}
    if funcs.count("¬") > 0: raise HTTPException(400, "К сожалению символ ¬, пока не поддерживается")
    for key in replacement.keys():
        funcs = funcs.replace(key, str(replacement.get(key)))
    url = f"https://tablica-istinnosti.ru/ru/kkn.php?dp={funcs}&fn=1&f3=1&fk=0&fd=0&fe=1&in="
    response = requests.get(url)
    if (response.status_code != 200): raise HTTPException(400, "Сервер не отвечает")
    bs = BeautifulSoup(response.text, "lxml")
    table = bs.find("table", {"style": "font-family:ddd;color:black;"})
    if table is None: raise HTTPException(400, "Неверный ввод")
    data = []
    for row in table.find_all("tr"):
        row_data = []
        for item in row.find_all("td"):
            row_data.append(item.text)
        data.append(row_data)
    return data

@app.get("/sdnf_sknf")
def sdnf_sknf(funcs: str, response: Response):
    response.headers["Cache-Control"] = "max-age=31536000, immutable"
    replacement = {"∧": 3, "∨": 4, "->": 5, "⇔": 6, "⊕": 7}
    if funcs.count("¬") > 0: raise HTTPException(400, "К сожалению символ ¬, пока не поддерживается")
    for key in replacement.keys():
        funcs = funcs.replace(key, str(replacement.get(key)))
    url = f"https://tablica-istinnosti.ru/ru/ssn.php?dp={funcs}&fn=1&f3=1&fk=0&fd=0&fe=1&in="
    response = requests.get(url)
    if (response.status_code != 200): raise HTTPException(400, "Сервер не отвечает")
    bs = BeautifulSoup(response.text, "lxml")
    sknf_table = bs.find(string=
                         "В результате, совершенная конъюнктивно-нормальная форма (СКНФ) нашей функции равна:") \
        .nextSibling
    sdnf_table = bs.find(string=
                         "В результате, совершенная дизъюнктивно-нормальная форма (СДНФ) нашей функции равна:") \
        .nextSibling
    if sknf_table is None: raise HTTPException(400, "Неверный ввод")
    if sdnf_table is None: raise HTTPException(400, "Неверный ввод")
    sknf = ""
    for item in sknf_table.find_all("td"):
        sknf += item.text
    sdnf = ""
    for item in sdnf_table.find_all("td"):
        sdnf += item.text
    return {"sknf": sknf, "sdnf": sdnf}

@app.get("/simplify")
def simplify(funcs: str, response: Response):
    response.headers["Cache-Control"] = "max-age=31536000, immutable"
    url = 'https://www.kontrolnaya-rabota.ru/krapi/add/input/?input={"expr":"' + funcs + '"}' \
    '&conf={"lang":"ru","format":"latex","use_latex":true,"choicer":true,"redirector":true,"img_width":3}&pod=mathlog.logic'
    response = requests.get(url, timeout=5)
    json = response.json()
    if json.get("error") is not None: raise HTTPException(400, "Неверный ввод")
    session = json.get("result").get('sessions').get('simplify') if json.get("result") is not None else None
    if session is None: raise HTTPException(400, "Неверный ввод")
    new_url = f"https://www.kontrolnaya-rabota.ru/krapi/v2/session/{session}/"
    response = requests.get(new_url)
    json = response.json()
    if json.get("error") is not None: raise HTTPException(400, "Ошибка при получении результата")
    result: str = json.get("result").get("simplify").get("subpods")[0].get("pprint")
    return {"result": result.upper()}


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
