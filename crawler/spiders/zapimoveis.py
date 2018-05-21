# -*- coding: utf-8 -*-
import scrapy
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
        self.links = []

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
            yield scrapy.Request(url=each, dont_filter=True, callback=self.parse)

    def parse(self, response):
        print(response.request.url)
        links = response.css('section.endereco a::attr("href")').extract()
        links = list(map(lambda x: x.split('/?')[0], links))
        m = list(set(self.links))
        l = list(set(links))
        needed = [item for item in l if item not in m]
        self.links = list(set(self.links + needed))
        for item in needed:
            yield from self.request_page(item)

    def request_page(self, link):
        yield scrapy.Request(link, dont_filter=True, callback=self.parse_page)

    def parse_page(self, response):
        id = response.css(
            'input[id="ofertaId"]::attr("data-value")').extract_first()
        street = response.css('h1.pull-left::text').extract()[1].strip()
        logradouro = response.css(
            'span.logradouro::text').extract_first()
        logradouro = logradouro.split(',')[0] if logradouro != None else ''
        price = response.css('div.value-ficha::text').extract()[1].strip()[3:]
        self.planilha.writerow([id, logradouro, street, price])
