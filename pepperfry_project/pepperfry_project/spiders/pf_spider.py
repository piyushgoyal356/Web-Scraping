import scrapy
import requests
import pandas as pd
import os
import json

class BookSpyder(scrapy.Spider):
    
    name = "pf_spider"
    
    def start_requests(self):
        
        #10 item types
        items = ["table", "sofa set", "Sectional sofa", "lights", "decor", "book shelves", "bean bags", "chair", "mattress", "blankets"]
        
        base_urls = [
            "https://www.pepperfry.com/site_product/search?q=",
        ]
        
        for base_url in base_urls:
            for item in items:
                url = base_url + '+'.join(item.split(' '))
                yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self,response):
        item_query = response.url.split("=")[1]
        item_foldername = '_'.join(item_query.split("+"))
        
        parent_dir = "D:/data science cb/web-scraping/pepperfry_project/data/"
        path = os.path.join(parent_dir,item_foldername)
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)
        
        #20 products of each item type
        products = response.css("a.clip-prd-dtl::attr(title)").getall()[:20]
        product_hrefs = response.css("a.clip-prd-dtl::attr(href)").getall()[:20]
        parent_dir_product = parent_dir+item_foldername
        product_paths = []
        
        for i in range(0,len(products)):
            
            #making folder name valid
            omits = '\ / : * ? " < > |'
            omit = omits.split(' ')
           
            for j in omit:
                while products[i].find(j) != -1:
                    p_string = list(products[i])
                    p_string[products[i].find(j)] = '-'
                    products[i] = "".join(p_string)
            
            path = ''
            try:
                path = os.path.join(parent_dir_product,products[i])
                os.mkdir(path)
            except WindowsError as e:
                #making duplicate names unique
                if e.winerror == 183:
                    products[i] = products[i]+'-'
                    path = os.path.join(parent_dir_product,products[i])
                    os.mkdir(path)
                print(e)

            product_paths.append(path)    
                
        for i in range(0,len(product_hrefs)):
            product_response = scrapy.Request(url=product_hrefs[i], callback=self.parse_product)
            product_response.cb_kwargs['prod_path'] = product_paths[i]
            yield product_response
            
            
    def parse_product(self,response,prod_path):
        
        img_urls = response.css("li.vipImage__thumb-each a::attr(data-img)").getall()
        if len(img_urls)>5:
            img_urls = img_urls[:5]
            
        detail_labels = response.css("span.v-prod-comp-dtls-listitem-label::text").getall()
        detail_label_values = response.css("span.v-prod-comp-dtls-listitem-value::text").getall()
        
        details = {}
        for i in range(0,len(detail_labels)):
            details[detail_labels[i]] = detail_label_values[i]
            
        details_path = os.path.join(prod_path,"details.json")
        with open(details_path,'w') as f:
            json.dump(details,f)
        
        for i in range(0,len(img_urls)):
            
            filename = os.path.join(prod_path,"image-%s.jpg"%i)
            img = requests.get(img_urls[i])
            
            with open(filename,'wb') as f:
                f.write(img.content)