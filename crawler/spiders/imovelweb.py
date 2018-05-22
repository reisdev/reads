# -*- coding: utf-8 -*-
import scrapy
import csv


class ImovelwebSpider(scrapy.Spider):
    name = 'imovelweb'
    allowed_domains = ['www.imovelweb.com.br/']
    start_urls = ['www.imovelweb.com.br/']

    def __init__(self, filename='new', city='goiania', state='go', *args, **kwargs):
        super(ImovelwebSpider, self).__init__()
        self.url_lotes = []
        self.filename = filename
        self.city = city
        self.state = state

    def fileLoader(self):
        try:
            file = open('results/%s.csv' % self.filename, 'w')
            self.planilha = csv.writer(
                file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            # The line below set the headers of the sheet, on the file creation
            self.planilha.writerow(
                ['Bairro', 'Rua', 'Preço', 'Latitude', 'Longitude', 'Link'])
        except ValueError:
            self.file = open('results/%s.csv' % self.filename, 'a')
            self.planilha = csv.writer(
                file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    def start_requests(self):
        url = "http://www.imovelweb.com.br/terrenos-venda-%s-%s" % (
            self.city, self.state)
        urls = []
        self.fileLoader()
        urls.append((url+'.html'))
        for i in range(1, 13):
            urls.append(url+'-pagina-%d.html' % i)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse_page(self, response):

        link = response.request.url
        # Get price
        price = response.css('strong.venta::text').extract_first()
        price = price[3:]

        lat = response.css('input[name="lat"]::attr("value")').extract_first()
        lng = response.css('input[name="lng"]::attr("value")').extract_first()

        lat = lat if (lat != None) else ''
        lng = lng if (lng != None) else ''

        # Get address
        tmp = response.css(
            'div.list.list-directions ul li::text').extract_first()
        if(tmp == None):
            tmp = ["Desconhecida", "Desconhecido"]
        else:
            tmp = tmp.split(',')
        if len(tmp) > 3:
            street = tmp[0].strip()
            neighborhood = tmp[2].strip()
        else:
            street = tmp[0].strip()
            neighborhood = tmp[1].strip()

        self.planilha.writerow([neighborhood, street, price, lat, lng, link])

    def request_page(self, link):
        yield scrapy.Request(url=link, callback=self.parse_page, dont_filter=True)

    def parse(self, response):
        links = response.css('li.aviso::attr("data-href")').extract()
        for item in links:
            yield from self.request_page(item)
