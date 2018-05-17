# -*- coding: utf-8 -*-
import scrapy
import csv


class ImovelwebSpider(scrapy.Spider):
    name = 'imovelweb'
    allowed_domains = ['www.imovelweb.com.br/']
    start_urls = ['www.imovelweb.com.br/']

    def __init__(self, filename='new', city='goiania', state='go', *args, **kwargs):
        super(ImovelwebSpider, self).__init__()
        self.urls = []
        self.filename = filename

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
        url = "http://www.imovelweb.com.br/terrenos-venda-goiania-go"
        self.fileLoader()
        self.urls.append((url+'.html'))
        for i in range(1, 13):
            self.urls.append(url+'-pagina-%d.html' % i)
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = response.css('li.aviso')
        for item in items:
            temp = {}
            temp['id'] = item.css('::attr("data-aviso")').extract_first()
            price = item.css(
                'span.aviso-data-price-value::text').extract_first()
            temp['price'] = price[3:]
            street = item.css(
                'span.aviso-data-location::text').extract_first().strip().replace('\t', '').replace('\n-', '').replace(',', '')
            temp['street'] = street
            location = item.css(
                'span.aviso-data-location span::text').extract_first().split(',')
            temp['neighborhood'] = location[0]
            self.planilha.writerow(
                [temp['id'], temp['neighborhood'], temp['street'], temp['price']])
