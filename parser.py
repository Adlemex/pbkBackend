from http.client import HTTPException

from bs4 import BeautifulSoup
import requests
# sdnf sknf url = 'https://tablica-istinnosti.ru/ru/ssn.php?dp=A3B4B4C4F4G4J4B4B4B4B4B4C&fn=0&f3=0&fk=0&fd=0&fe=0&in='
funcs = "A7B"
replacement = {"∧": 3, "∨": 4, "->": 5, "⇔": 6, "⊕": 7}
if funcs.count("¬") > 0: raise HTTPException(400, "К сожалению символ ¬, пока не поддерживается")
for key in replacement.keys():
    funcs = funcs.replace(key, str(replacement.get(key)))
url = f"https://tablica-istinnosti.ru/ru/ssn.php?dp={funcs}&fn=1&f3=1&fk=0&fd=0&fe=1&in="
response = requests.get(url)
if (response.status_code != 200): raise HTTPException(400, "Сервер не отвечает")
bs = BeautifulSoup(response.text, "lxml")
sknf_table = bs.find(string=
                     "В результате, совершенная конъюнктивно-нормальная форма (СКНФ) нашей функции равна:")\
    .nextSibling
sdnf_table = bs.find(string=
                     "В результате, совершенная дизъюнктивно-нормальная форма (СДНФ) нашей функции равна:")\
    .nextSibling
if sknf_table is None: raise HTTPException(400, "Неверный ввод")
if sdnf_table is None: raise HTTPException(400, "Неверный ввод")
sknf = ""
for item in sknf_table.find_all("td"):
    sknf += item.text
sdnf = ""
for item in sdnf_table.find_all("td"):
    sdnf += item.text
print(sdnf)
print(sknf)