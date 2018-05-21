# -*- coding: utf-8 -*-
import scrapy


class VivarealSpider(scrapy.Spider):
    name = 'vivareal'
    allowed_domains = ['www.vivareal.com.br']
    start_urls = ['http://www.vivareal.com.br/']

    def start_requests(self):
        main = 'https://www.vivareal.com.br/venda/goias/goiania/lote-terreno_residencial/'
        urls = [main]
        for i in range(2, 31):
            urls.append((main+'?pagina=%d' % i))
        for url in urls:
            yield scrapy.Request(url, callback=self.request_pages)

    def request_pages(self, response):
        pass
