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
        pass
