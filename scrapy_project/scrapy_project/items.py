import scrapy


class ScrapyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()