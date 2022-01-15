from bs4 import BeautifulSoup
import requests
import re

search_term = input("What product do you want to search for?\n")
while search_term is None:
    search_term = input("What product do you want to search for?\n")

url = f"https://www.newegg.com/p/pl?d={search_term}"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

page_text = doc.find(class_="list-tool-pagination-text").strong
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

for page in range(1, pages + 1):
    url = f"https://www.newegg.com/p/pl?d={search_term}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    items = doc.find_all('a', text=re.compile(search_term))

# item coount
# print(search_term + " count: " + str(len(items)))
