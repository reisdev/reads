# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv

from datetime import datetime as date


class lotePipeline(object):
    def __init__(self):
        self.filename = date.now().strftime('%d-%m-%Y %H:%M:%S')
        try:
            file = open('results/%s.ods' % self.filename, 'w')
            self.planilha = csv.writer(
                file, delimiter='@', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            # The line below set the headers of the sheet, on the file creation
            self.planilha.writerow(
                ['ID', 'Endereço', 'Preço', 'Latitude', 'Longitude', 'Link'])
        except ValueError:
            self.file = open('results/%s.ods' % self.filename, 'a')
            self.planilha = csv.writer(
                file, delimiter='@', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    def process_item(self, item, spider):
        tmp = list(item.values())
        self.planilha.writerow(tmp)
        return tmp
