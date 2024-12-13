import scrapy


class ScrapyprojectItem(scrapy.Item):
    # Define fields for your project-specific item here
    pass


class ProductItem(scrapy.Item):
    # Define the fields for the scraped product data
    name = scrapy.Field()           # Property title
    rating = scrapy.Field()         # Rating of the property
    location = scrapy.Field()       # Address or location description
    latitude = scrapy.Field()       # Latitude of the property
    longitude = scrapy.Field()      # Longitude of the property
    room_type = scrapy.Field()      # Room type information
    price = scrapy.Field()          # Price details
    image_url = scrapy.Field()      # URL for the property image
    url = scrapy.Field()            # Link to the property page
