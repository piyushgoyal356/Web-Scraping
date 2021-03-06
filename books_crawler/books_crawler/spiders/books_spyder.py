import scrapy
import pandas as pd

class BookSpyder(scrapy.Spider):
    
    name = "books_spyder"
    
    def start_requests(self):
        urls = [
            "http://books.toscrape.com/catalogue/page-1.html",
        ]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self,response):
        page_id = response.url.split("-")[1][:-5]
        filename = "book-%s.json"%page_id
        
        image_url = response.css("img.thumbnail::attr(src)").getall()
        book_title = response.css("article.product_pod h3 a::attr(title)").getall()
        product_price = response.css("p.price_color::text").getall()
        
        for i in range(0,len(image_url)):
            yield {
                'image_url' : image_url[i],
                'book_title' : book_title[i],
                'product_price' : product_price[i],
            }
        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        
#        with open(filename,'wb') as f:
#            f.write(response.body)
#        self.log("Saved file %s"%filename)