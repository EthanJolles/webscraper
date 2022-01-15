
from bs4 import BeautifulSoup
import requests
import re
from xlwt import Workbook

search_term = input("What product do you want to search for?\n")
while search_term is None:
    search_term = input("What product do you want to search for?\n")

url = f"https://www.newegg.com/p/pl?d={search_term}"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

page_text = doc.find(class_="list-tool-pagination-text").strong
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

items_found = {}

for page in range(1, pages + 1):
    url = f"https://www.newegg.com/p/pl?d={search_term}&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    items = div.find_all(text=re.compile(search_term))

    for item in items:
        parent = item.parent
        if parent.name != 'a':
            continue
        link = parent['href']
        next_parent = item.find_parent(class_="item-container")
        price = next_parent.find(class_="price-current").strong.text

        items_found[item] = {
            "link": link,
            "price": price
         }

# Workbook is created
wb = Workbook()

# add_sheet is used to create sheet.
sheet = wb.add_sheet('Sheet 1')

sheet.write(0, 0, 'ITEM')
sheet.write(0, 1, 'LINK')
sheet.write(0, 2, 'PRICE')


row_counter = 0
sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])
for item in sorted_items:
    row_counter+=1
    sheet.write(row_counter, 0, item[0])
    sheet.write(row_counter, 1, item[1]['link'])
    sheet.write(row_counter, 2, item[1]['price'])

wb.save(f"newegg_products/{search_term}.xls")
