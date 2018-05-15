# -*- coding: utf-8 -*-
import scrapy
import csv
from scrapy.selector import Selector


class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['zapmoveis.com.br']

    def __init__(self, filename='new.csv', city='goiania', state='go', init=0, end=10, *args, **kwargs):
        super(MainSpider, self).__init__(*args, **kwargs)
        self.init = init
        self.end = end
        self.filename = filename
        self.url = 'https://www.storiaimoveis.com.br/comprar/'
        self.city = city
        self.state = state

    def start_requests(self):
        self.fileLoader()

        for i in range(int(self.init), int(self.end)):
            tmp = self.url+"%s-%s?page=%d" % (self.city, self.state, i)
            yield scrapy.Request(url=tmp, callback=self.parse)

    def fileLoader(self):
        try:
            file = open('results/%s.csv' % self.filename, 'w')
            self.planilha = csv.writer(
                file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            self.planilha.writerow(
                ['Localização', 'Preço', 'Quantidade de Quartos'])
        except ValueError:
            self.file = open('results/%s.csv' % self.filename, 'a')
            self.planilha = csv.writer(
                file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    def parse(self, response):
        divs = response.css('div[role="link"]')
        quartos = divs.css(
            'span[data-ui-tracker="OFFER_BEDROOMS"]::text').extract()
        prices = divs.css('div[data-ui-tracker="OFFER_PRICE"]::text').extract()
        locais = divs.css('div span[class="f8 light-gray"]::text').extract()

        for i in range(0, len(quartos)):
            self.planilha.writerow([locais[i], prices[i], quartos[i]])
