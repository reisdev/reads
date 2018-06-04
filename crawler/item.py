import scrapy


class Lote(scrapy.Item):
    id = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    link = scrapy.Field()
