# -*- coding: utf-8 -*-
import scrapy


class ZapimoveisSpider(scrapy.Spider):
    name = 'zapimoveis'
    allowed_domains = ['zapimoveis.com.br']
    start_urls = ['http://zapimoveis.com.br/']

    def start_requests(self):
        url = 'https://www.zapimoveis.com.br/venda/terreno-padrao/go+goiania/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = response.css('article.minificha')
        for item in items:
            # Extracts the price
            price = item.css('div.preco strong::text').extract_first()
            price = price[3:]
            # Extracts the address
            address = item.css('section.endereco')
            neighborhood = address.css('strong::text').extract_first()
            street = address.css(
                'span[itemprop="streetAddress"]::text').extract_first()

            print(price, neighborhood, street)
