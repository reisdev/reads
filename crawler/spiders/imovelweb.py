# -*- coding: utf-8 -*-
import scrapy


class ImovelwebSpider(scrapy.Spider):
    name = 'imovelweb'
    allowed_domains = ['www.imovelweb.com.br/']
    start_urls = ['www.imovelweb.com.br/']

    def __init__(self, city='goiania', state='go', *args, **kwargs):
        super(ImovelwebSpider, self).__init__()

    def start_requests(self):
        url = "http://www.imovelweb.com.br/terrenos-venda-goias.html"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = response.css('li.aviso')
        for item in items:
            price = item.css(
                'span.aviso-data-price-value::text').extract_first()
            location = item.css(
                'span.aviso-data-location span::text').extract_first()

            print(price, location)
