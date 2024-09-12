from bs4 import BeautifulSoup
import requests, json, time


# site = requests.get("https://uz.wikipedia.org/wiki/O%CA%BBzbekiston")
# print(site.text)

# with open("wiki.html", "w", encoding="UTF8") as file:
#     file.write(site.text)

with open("wiki.html", encoding="UTF8") as file:
    html = file.read()

htmldom = BeautifulSoup(html, "lxml")
items = htmldom.find("div", class_="mw-content-ltr mw-parser-output").find_all("p")
mundarija = []

for it in items:
    mundarija.append(it.find_all("sup", class_="reference"))
print(mundarija)

