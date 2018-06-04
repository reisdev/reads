# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import csv
import json
import requests
from crawler.item import Lote

decoder = json.JSONDecoder()
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep


class VivarealSpider(scrapy.Spider):
    name = 'vivareal'
    allowed_domains = ['www.vivareal.com.br']

    def __init__(self, *args, **kwargs):
        super(VivarealSpider, self).__init__(*args, **kwargs)
        self.main = 'https://www.vivareal.com.br'
        self.links = []
        self.driver = webdriver.Firefox()

    def start_requests(self):
        url = self.main + '/venda/goias/goiania/lote-terreno_residencial/'
        yield scrapy.Request(url=url, callback=self.parse_page)

    def storeLinks(self, links):
        for link in links:
            self.links.append(link.get_attribute('href'))

    def parse_page(self, response):
        self.driver.get(response.url)
        while True:
            try:
                next = WebDriverWait(self.driver, 10)
                links = self.driver.find_elements_by_xpath(
                    '//a[@class="property-card__main-link js-carousel-link"]')
                self.storeLinks(links)
                next.until(EC.element_to_be_clickable(
                    (By.XPATH, '//a[@title="Próxima página"]'))).click()
                sleep(3)
            except Exception:
                print('It has ended')
                break
        self.driver.close()
        for item in self.links:
            yield scrapy.Request(url=item, callback=self.parse)

    def parse(self, response):
        link = response.url.split('id-')[1]
        id = link.split('/')[0]
        link = response.url
        price = response.xpath(
            '//span[@class="aI js-detail-sale-price"]/text()').extract_first()[3:]
        address = response.xpath(
            '//a[@class="U js-title-location"]/text()').extract_first()
        maps = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + \
            address+'&key=AIzaSyBhJ7IKQWwiNS-vQaAhIleUq1ozFJy0Glc'
        req = requests.get(maps)
        try:
            req = decoder.decode(req.text)[
                'results'][0]['geometry']['location']
            lat = req['lat']
            lon = req['lng']
        except (RuntimeError, NameError):
            lat = ''
            lon = ''
        novo_lote = Lote(id=id, address=address, price=price,
                         lat=lat, lon=lon, link=link)
        yield novo_lote
