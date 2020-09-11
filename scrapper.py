"""

Scrapper for scraping products from product listing page of ebay.com

"""

from Capstone.models import Product
from bs4 import BeautifulSoup
import requests

def scrap(url,category):
    results=requests.get(url)
    soup=BeautifulSoup(results.text,features="html.parser")
    ol=soup.find("ul",{"class":"srp-results"})
    items = ol.find_all("li",{"class":"s-item"})

    for i in items:
        name = i.find("h3",{"class":"s-item__title"}).text
        img = i.find('img').attrs["src"]

        if img[len(img)-1]=="f":
            img = i.find('img').attrs["data-src"]
        url = i.find("div",{"class":"s-item__image"}).find("a").attrs["href"]
        rating = i.find("span",{"class":"b-starrating__star"})
        price = i.find("span",{"class":"s-item__price"})
        shipping_price = i.find("span",{"class":"s-item__logisticsCost"}).text
	
	# If Price is not mentioned skip that product.
        if price == None:
            continue
        else:
            price = price.text
	
	# Store Rating as integer
        if rating == None : 
            rating = 0
        else:
            rating = int(rating.find("span").text[0])
        xprice = float(price.split(' ')[1].replace(',',''))

	# Change Shipping Price to 0 incase of Free Shipping
        if shipping_price.lower().strip().startswith("free"):
            total_cost = int(xprice)
        else:
            xshipping_price = float(shipping_price.split(' ')[1].replace(',',''))
            total_cost = int(xprice + xshipping_price)

	# Create and save objects to the db.
        p = Product.objects.create(name = name, img_link = img, rating = rating, price = price, url = url, category = category, shipping_price = shipping_price, total_cost= total_cost )
        p.save()
        print(f"Inserted {name} ")


