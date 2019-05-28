# -*- coding: utf-8 -*-
import scrapy
import csv
from selenium import webdriver
from time import sleep

from crawler.item import Lote


class ZapimoveisSpider(scrapy.Spider):
    name = 'zapimoveis'
    allowed_domains = ['zapimoveis.com.br']

    def __init__(self, filename='new', city='goiania', state='go', init=1, end=10, *args, **kwargs):
        super(ZapimoveisSpider, self).__init__(*args, **kwargs)
        self.init = int(init)
        self.end = int(end)
        self.url = 'https://www.zapimoveis.com.br/venda/terreno-padrao'
        self.city = city
        self.state = state
        self.driver = webdriver.Firefox()
        self.links = []

    def start_requests(self):
        url = 'https://www.zapimoveis.com.br/venda/terreno-padrao/go+goiania/#{"pagina":"1","possuiendereco":"True"}'
        yield scrapy.Request(url, callback=self.parse)

    def storeLink(self, links):
        for item in links:
            self.links.append(item.get_attribute('href'))

    def parse(self, response):
        self.driver.get(response.url)
        position = int(self.driver.find_element_by_name(
            'txtPaginacao').get_attribute('value'))
        while True:
            position = int(self.driver.find_element_by_name(
                'txtPaginacao').get_attribute('value'))
            next = self.driver.find_element_by_id('proximaPagina')
            max = int(self.driver.find_element_by_xpath(
                '//span[@class="pull-right num-of"]').text[3:])
            try:
                links = self.driver.find_elements_by_xpath(
                    '//section[contains(@class,"endereco")]/a')
                self.storeLink(links)
                self.driver.execute_script("arguments[0].click()", next)
                sleep(3)
                if position == max:
                    break
            except Exception as err:
                print(err)
                break
        self.driver.close()
        for item in self.links:
            yield scrapy.Request(url=item, callback=self.parse_page)

    def parse_page(self, response):
        link = response.url
        id = response.css(
            'input[name="CodImovel"]::attr("value")').extract_first()
        street = response.css('h1.pull-left::text').extract()[1].strip()
        street = street.split(',')[0]
        logradouro = response.css(
            'span.logradouro::text').extract_first()
        logradouro = logradouro.split(',')[0] if logradouro != None else ''
        address = street + ' - ' + logradouro
        price = response.css(
            'div.value-ficha::text').extract()[1].strip()[3:].split(',')[0]
        coord = response.css(
            'div[id="imgMapaGoogleEstatico"]::attr("onclick")').extract_first()
        if(coord != None):
            coord = coord.split('(')[1].split(')')[0].split(',')
            lat = coord[0]
            lon = coord[1]
        else:
            lat = ''
            lon = ''
        novo_lote = Lote(id=id, address=address, price=price,
                         lat=lat, lon=lon, link=link)
        yield novo_lote
