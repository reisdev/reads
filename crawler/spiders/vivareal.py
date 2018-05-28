# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver

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
        url = self.main + '/venda/goias/goiania/lote-terreno_residencial'
        yield scrapy.Request(url=url, callback=self.parse)

    def storeLinks(self, links):
        for link in links:
            self.links.append(self.main + link.get_attribute('href'))

    def parse(self, response):
        self.driver.get(response.url)
        while True:
            try:
                next = WebDriverWait(self.driver, 10)
                next.until(EC.element_to_be_clickable(
                    (By.XPATH, '//a[@title="Próxima página"]'))).click()
                sleep(5)
                links = self.driver.find_elements_by_xpath(
                    '//a[@class="property-card__main-link js-carousel-link"]')
                self.storeLinks(links)
            except Exception:
                print('It has ended')
                break
        self.driver.close()
        print('Terminou. %s links capturados' % len(self.links))
