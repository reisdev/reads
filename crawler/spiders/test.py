# -*- coding: utf-8 -*-
import scrapy
import csv
from scrapy.selector import Selector

class GoogleSpider(scrapy.Spider):
    name = 'test'
    allowed_domains=['zapmoveis.com.br']
    
    def start_requests(self):
        
        url= 'https://www.storiaimoveis.com.br/comprar/curitiba-pr'
        
        for i in range(0,10):
            tmp = url+"?page=%d" % i
            yield scrapy.Request(url=tmp, callback=self.parse)

    def parse(self, response):
        divs = response.css('div[role="link"]')
        quartos = divs.css('span[data-ui-tracker="OFFER_BEDROOMS"]::text').extract()
        prices = divs.css('div[data-ui-tracker="OFFER_PRICE"]::text').extract()
        locais = divs.css('div span[class="f8 light-gray"]::text').extract()
        
        with open('../results/test.csv','a') as csvfile:
            planilha = csv.writer(csvfile,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
            
            for i in range(0,len(quartos)):
                planilha.writerow([locais[i],prices[i],quartos[i]])
                
        
