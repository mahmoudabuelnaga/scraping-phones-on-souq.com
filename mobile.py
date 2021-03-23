from bs4 import BeautifulSoup
import requests
import csv
from itertools import zip_longest

link_categories = []
items_names = []
items_prices = []
links = []
images_src = []

result = requests.get("https://egypt.souq.com/eg-en/eg-mobile-tablet/c/?ref=nav")
src = result.content
soup = BeautifulSoup(src, "html.parser")

div = soup.find_all("div",{"class":"columns small-6 medium-3 large-3"})

for i in range(12):
    link_categories.append(div[i].find("a").attrs['href'])
    print(div[i].find("a").attrs['href'])


for link_category in link_categories:
    result = requests.get(link_category)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    item_link = soup.find_all("div",{"class":"col col-info item-content"})
    img_src = soup.find_all("div", {"class":"col col-image relative discount-wrap"})
    print(item_link)
    print(img_src)

    for item_name in soup.find_all("h1",{"class":"itemTitle"}):
        items_names.append(item_name.text.strip())
        print(item_name.text.strip())
        
    for item_price in soup.find_all("div",{"class":"price-inline"}):
        items_prices.append(item_price.text.strip())
        print(item_price.text.strip())
    
    for i in soup.find_all("div",{"class":"col col-info item-content"}):
        if 'href' in i.attrs:
            links.append(i.find(      
                "a", {"class":"itemLink sk-clr2 sPrimaryLink"}).attrs['href'])
            print(i.find(      
                "a", {"class":"itemLink sk-clr2 sPrimaryLink"}).attrs['href'])
        else:
            continue

        if 'src' in i.attrs:
            images_src.append(
                i.find(
                    "img", {"class":"img-size-medium lazy-loaded imageUrl"}).attrs['src'])
            print(i.find(
                "img", {"class":"img-size-medium lazy-loaded imageUrl"}).attrs['src'])

        else:
            continue



file_list = [items_names, items_prices, links, images_src]
exported = zip_longest(*file_list)
with open("/home/mahmoudaboelnaga/Desktop/developer/mobile_items.csv", "w") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Items Names", "Items Prices", "Links", "Images Src"])
    wr.writerows(exported)