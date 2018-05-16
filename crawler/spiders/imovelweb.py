# -*- coding: utf-8 -*-
import scrapy
import csv


class ImovelwebSpider(scrapy.Spider):
    name = 'imovelweb'
    allowed_domains = ['www.imovelweb.com.br/']
    start_urls = ['www.imovelweb.com.br/']

    def __init__(self, filename='new', city='goiania', state='go', *args, **kwargs):
        super(ImovelwebSpider, self).__init__(*args, **kwargs)
        self.counter = 0
        self.filename = filename

    def start_requests(self):

        self.fileLoader()

        url = "http://www.imovelweb.com.br/terrenos-venda-goias"
        for i in range(1, 45):
            temp = url+'-pagina-%d.html' % i
            yield scrapy.Request(url=temp, callback=self.parse)
        print("Number of results: %d" % self.counter)

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

    def parse(self, response):
        items = response.css('li.aviso')
        for item in items:
            self.counter += 1
            price = item.css(
                'span.aviso-data-price-value::text').extract_first()
            price = price[3:]
            location = item.css(
                'span.aviso-data-location span::text').extract_first().split(', ')

            self.planilha.writerow([location[0], location[1], price])
