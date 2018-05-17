# -*- coding: utf-8 -*-
import scrapy
import csv


class StoriaSpider(scrapy.Spider):
    name = 'storia'
    allowed_domains = ['zapmoveis.com.br']

    def __init__(self, filename='new', city='goiania', state='go', init=1, end=10, *args, **kwargs):
        super(StoriaSpider, self).__init__(*args, **kwargs)
        self.init = init
        self.end = end
        self.filename = filename
        self.url = 'https://www.storiaimoveis.com.br/comprar/'
        self.city = city
        self.state = state

    def start_requests(self):
        self.fileLoader()

        for i in range(int(self.init), int(self.end)):
            tmp = self.url + "%s-%s/terreno" % (self.city, self.state)
            # The line below is to prevent the request page=1,
            # that causes a redirection and then, the request
            # of the first page isn't processed
            tmp += ("?page=%d" % i) if (i != 1) else ''
            yield scrapy.Request(url=tmp, callback=self.parse)

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
        announces = response.css('div[role="link"]')

        for item in announces:
            price = item.css(
                'div[data-ui-tracker="OFFER_PRICE"]::text').extract_first()
            price = price[3:]  # This line removes the 'R$ ' from the string
            local = item.css(
                'div span[class="f8 light-gray"]::text').extract_first().split(' - ')
            self.planilha.writerow([local[1], local[0], price])
