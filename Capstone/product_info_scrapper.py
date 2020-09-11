"""

Scrapper for scrapping product details from product page of Ebay

"""
from bs4 import BeautifulSoup
import requests

def product_details(url):
    print("\n\nScrap started")
    print("Product Url: ",url,"\n")

    # Get the contents of the url and change it into Soup Objects
    results=requests.get(url)
    i=BeautifulSoup(results.text,features="html.parser")

    product_name = i.find("h1",{"class":"product-title"})
    product_img = i.find_all('div',{"class":'app-filmstrip__owl-carousel'})
    p_images = []
    img_strip = [] 

    # Obtaining links of the images from carousel strip of the product
    if product_img == []:
    
        main = i.find("img",{"id":"icImg"}).attrs["src"]
        pivot = main.split('-')[-1][1:].split('.')[0] 
        product_img = i.find("div",{"id":"vi_main_img_fs" })

        if product_img == None:
            
            product_img = main
            img_strip.append(product_img)
            p_images.append(product_img)
        
        else:
        
            product_img = product_img.find_all('img')
        
            for img in product_img:
                img_strip.append(img.attrs["src"])
                src = img.attrs["src"].split('-')
                src[-1] = src[-1][0] + pivot + ".jpg"
                img_src='-'.join(src)
                p_images.append(img_src) 
    
    else:
    
        product_img = product_img[-1].find_all('img')
    
        for img in product_img:
            img_src = img.attrs["data-originalimg"]
            img_strip.append(img.attrs["src"])
            p_images.append(img_src)
    
    # Get the product name  the product page.
    if product_name == None:
        
        product_name = i.find("h1",{"id":"itemTitle"})
        
        if product_name == None:
            product_name = i.find("h1",{"class":"vi-title__main"}).find(recursive=True,text=True)
        
        else:
            product_name = product_name.find(recursive=False,text=True)
    
    else:
        product_name = product_name.text

    data = {}   
    keys = []
    values = []
    titles = []        
    
    product_specification = i.find("section",{"class":"product-spectification"})

    # Collect the product specification.

    if product_specification == None:
        
        x=[]
        product_specification = i.find("div",{"class":"section"})
        
        if product_specification == None:

            product_specification = i.find("div",{"id":"vi-frag-btfcontainer-w1"}).find_all('div',{"class":"left"})
            
            for k in product_specification:
                x.append(k.find(text=True))
                print(k.find(text=True))
            
            for j in range(len(x)):
            
                if j%2==0:
                    keys.append(x[j])
                    print(x[j],end=' --> ')
                else:
                    if 'See the seller' in x[j]:
                            x[j] = x[j].split('See the seller')[0]
                    values.append(x[j])
                    print(x[j],end='\n')            
                    print("------------------------------") 

        else:    
            
            product_specification = product_specification.find_all("tr")
        
            for i in product_specification:
                x=i.find_all("td")
                j=0
            
                while j<len(x):                
                    x[j]=x[j].text.strip()
                    if x[j]=='':
                        break
                    if x[j][len(x[j])-1]==":":                
                        x[j]=x[j][:len(x[j])-1]
                    if j%2!=0:
                        if 'See the seller' in x[j]:
                            x[j] = x[j].split('See the seller')[0]
                        values.append(x[j])
                        print(x[j],end='\n')            
                        print("------------------------------") 
                    else:
                        keys.append(x[j])
                        print(x[j],end=' --> ')
                    j=j+1
        
        for i in range(len(keys)):
            data[keys[i]] = values[i]
    else:
        product_specification_list = product_specification.find_all("div",{"class":"spec-row"})
        for j in product_specification_list:
            title = j.find("h2").text
            titles.append(title)
            data[title]={}
            print('\033[1m' + title) 
            print("\n") 
            if title == "Product Information":
                data[title]=j.find("li").text
                print(j.find("li").text) 
                print("\n")
                continue
            for k in j.find_all("li"):
                name = k.find("div",{"class":"s-name"}).text
                value = k.find("div",{"class":"s-value"}).text
                data[title][name] = value 
                print(name,"--->",value) 
                print("-------------------------------")
            
            print("\n")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("\n\n")
        print("list of elements",data,'\n\n\n')
        
    return {"product_title": product_name , "product_images": p_images, "img":img_strip ,"spec_titles":titles , "product_spec":data}  

