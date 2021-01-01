import scrapy
import pandas as pd
import os

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
        parent_dir_product = parent_dir+item_foldername
        
        for i in range(0,len(products)):
            
            #making folder name valid
            omits = '\ / : * ? " < > |'
            omit = omits.split(' ')
           
            for j in omit:
                while products[i].find(j) != -1:
                    p_string = list(products[i])
                    p_string[products[i].find(j)] = '-'
                    products[i] = "".join(p_string)
            
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
#        
#        image_url = response.css("img.thumbnail::attr(src)").getall()
#        book_title = response.css("article.product_pod h3 a::attr(title)").getall()
#        product_price = response.css("p.price_color::text").getall()
#        
#        for i in range(0,len(image_url)):
#            yield {
#                'image_url' : image_url[i],
#                'book_title' : book_title[i],
#                'product_price' : product_price[i],
#            }
        
#        next_page = response.css('li.next a::attr(href)').get()
#        if next_page is not None:
#            next_page = response.urljoin(next_page)
#            yield scrapy.Request(next_page, callback=self.parse)
#        
#        with open(filename,'wb') as f:
#            f.write(response.body)
#        self.log("Saved file %s"%filename)