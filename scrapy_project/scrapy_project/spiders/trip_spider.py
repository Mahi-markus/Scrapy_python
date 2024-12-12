import scrapy
from scrapy_project.items import ProductItem

class TripSpider(scrapy.Spider):
    name = "trip"
    allowed_domains = ["scrapingcourse.com"]
    start_urls = ["https://www.scrapingcourse.com/ecommerce/"]

    def parse(self, response):
        products = response.css("li.product")
        for product in products:
            item = ProductItem()
            item['name'] = product.css("h2::text").get(default="No Name")
            item['image_url'] = response.urljoin(product.css("img::attr(src)").get(default=""))
            item['price'] = "".join(product.css(".price *::text").getall()).strip()
            item['url'] = response.urljoin(product.css("a::attr(href)").get(default=""))
            yield item

        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

