import scrapy


class ScrapyprojectItem(scrapy.Item):
    # Define fields for your project-specific item here
    pass


class ProductItem(scrapy.Item):
    # Define the fields for the scraped product data
    hotel_id = scrapy.Field()       # Unique ID of the hotel
    hotel_name = scrapy.Field()     # Name of the hotel
    rating = scrapy.Field()         # Hotel rating
    address = scrapy.Field()        # Hotel address
    latitude = scrapy.Field()       # Latitude of the hotel
    longitude = scrapy.Field()      # Longitude of the hotel
    room_type = scrapy.Field()      # Room type information
    price = scrapy.Field()          # Room price
    image_url = scrapy.Field()      # URL for the hotel image