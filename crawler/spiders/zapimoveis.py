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

    def fileLoader(self):
        try:
            file = open('results/%s.csv' % self.filename, 'w')
            self.planilha = csv.writer(
                file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            # The line below set the headers of the sheet, on the file creation
            self.planilha.writerow(
                ['Bairro', 'Rua', 'Preço'])
        except ValueError:
            self.file = open('results/%s.csv' % self.filename, 'a')
            self.planilha = csv.writer(
                file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    def start_requests(self):
        self.fileLoader()
        for i in range(self.init, self.end):
            parameters = '?__zt=pdpnumber:40#{"precomaximo":"2147483647","parametrosautosuggest":[{"Bairro":"","Zona":"","Cidade":"","Agrupamento":"","Estado":"GO"}],"pagina":"%d","ordem":"Relevancia","paginaOrigem":"ResultadoBusca","semente":"1396422568","formato":"Lista"}' % i
            url = self.url + '/%s+%s/%s' % (self.state, self.city, parameters)
            yield scrapy.Request(url, callback=self.parse_items)

    def parse_items(self, response):
        items = response.css('article.minificha')
        for item in items:
            self.counter += 1
            # Extracts the price
            price = item.css('div.preco strong::text').extract_first()
            price = price[3:]
            # Extracts the address
            address = item.css('section.endereco')
            neighborhood = address.css('strong::text').extract_first()
            street = address.css(
                'span[itemprop="streetAddress"]::text').extract_first()
            self.planilha.writerow([neighborhood, street, price])
