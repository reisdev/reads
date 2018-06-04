# -*- coding: utf-8 -*-
import scrapy
import csv
from crawler.item import Lote


class ImovelwebSpider(scrapy.Spider):
    name = 'imovelweb'
    allowed_domains = ['www.imovelweb.com.br/']
    start_urls = ['www.imovelweb.com.br/']

    def __init__(self, filename='new', city='goiania', state='go', *args, **kwargs):
        super(ImovelwebSpider, self).__init__()
        self.domain = 'http://www.imovelweb.com.br'
        self.city = city
        self.state = state

    def start_requests(self):
        url = "http://www.imovelweb.com.br/terrenos-venda-%s-%s" % (
            self.city, self.state)
        urls = []
        urls.append((url+'.html'))
        for i in range(1, 13):
            urls.append(url+'-pagina-%d.html' % i)
        for item in urls:
            yield scrapy.Request(url=item, callback=self.parse_page, dont_filter=True)

    def parse(self, response):
        # Get link
        link = response.request.url

        # Get id
        id = response.css(
            'div[class="content   "]::attr("data-aviso")').extract_first()

        # Get price
        price = response.css('strong.venta::text').extract_first()
        price = price[3:]

        # Get coordinates
        lat = response.css('input[name="lat"]::attr("value")').extract_first()
        lng = response.css('input[name="lng"]::attr("value")').extract_first()

        lat = lat if (lat != None) else ''
        lng = lng if (lng != None) else ''

        # Get address
        address = response.css(
            'div.list.list-directions ul li::text').extract_first()
        if(address == None):
            address = 'Não informado'
        novo_lote = Lote(id=id, address=address, price=price,
                         lat=lat, lon=lng, link=link)
        yield novo_lote

    def request_page(self, link):
        yield scrapy.Request(url=link, callback=self.parse, dont_filter=True)

    def parse_page(self, response):
        links = response.css('li.aviso::attr("data-href")').extract()
        for item in links:
            yield from self.request_page(self.domain+item)
