# -*- coding: utf-8 -*-
import scrapy
import urllib.parse as urlparse
import csv


class ZapimoveisSpider(scrapy.Spider):
    name = 'zapimoveis'
    allowed_domains = ['zapimoveis.com.br']

    def __init__(self, filename='new', city='goiania', state='go', init=1, end=10, *args, **kwargs):
        super(ZapimoveisSpider, self).__init__(*args, **kwargs)
        self.init = int(init)
        self.end = int(end)
        self.filename = filename
        self.url = 'https://www.zapimoveis.com.br/venda/terreno-padrao'
        self.city = city
        self.state = state
        self.counter = 0
        self.urls = []
        self.items = []

    def fileLoader(self):
        try:
            file = open('results/%s.csv' % self.filename, 'w')
            self.planilha = csv.writer(
                file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            # The line below set the headers of the sheet, on the file creation
            self.planilha.writerow(
                ['ID', 'Bairro', 'Rua', 'Preço'])
        except ValueError:
            self.file = open('results/%s.csv' % self.filename, 'a')
            self.planilha = csv.writer(
                file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    def start_requests(self):
        self.fileLoader()
        for i in range(self.init, self.end):
            parameters = '?__zt=pdpnumber:40# {"pagina":"%d"}' % i
            self.urls.append(self.url + '/%s+%s/%s' %
                             (self.state, self.city, parameters))
        for each in self.urls:
            yield scrapy.Request(url=each, callback=self.parse_items)

    def parse_items(self, response):
        announces = response.css('article.minificha')
        self.items = []
        for item in announces:
            temp = {}
            self.counter += 1
            # Extracts the price
            price = item.css('div.preco strong::text').extract_first()
            temp['price'] = price[3:]
            # Extracts the id
            section = item.css(
                'section.caracteristicas a::attr("href")').extract_first()
            temp['url'] = section
            pagina = section.split('=')
            if(len(pagina) == 2):
                temp['pagina'] = pagina[1]
            else:
                temp['pagina'] = ''
            temp['id'] = section.split('/')[5]
            # Extracts the address
            address = item.css('section.endereco')
            temp['neighborhood'] = address.css('strong::text').extract_first()
            temp['street'] = address.css(
                'span[itemprop="streetAddress"]::text').extract_first()
            if [temp['id'], temp['pagina']] in self.items:
                print('Já tem')
            else:
                self.items.append([temp['id'], temp['pagina']])
                self.planilha.writerow(
                    [temp['id'], temp['neighborhood'], temp['street'], temp['price'], temp['pagina']])
