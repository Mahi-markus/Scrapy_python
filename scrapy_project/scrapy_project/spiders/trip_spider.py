import scrapy
import json
from scrapy_project.items import ProductItem


class TripSpider(scrapy.Spider):
    name = "trip"
    allowed_domains = ["uk.trip.com"]
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
        # Extract embedded JSON from JavaScript
        json_data = self.extract_json_data(response)

        if json_data:
            hotels_data = []  # To store filtered hotel data

            cities = json_data.get("initData", {}).get("htlsData", {}).get("inboundCities", [])
            for city in cities:
                if city.get("name") == "Dhaka":  # Filter by specific city
                    hotels = city.get("recommendHotels", [])
                    for hotel in hotels:
                        hotel_data = {
                            "name": hotel.get("hotelName", "No Name"),
                            "rating": hotel.get("rating", "No Rating"),
                            "location": hotel.get("fullAddress", "No Location"),
                            "latitude": hotel.get("lat", "No Latitude"),
                            "longitude": hotel.get("lon", "No Longitude"),
                            "room_type": hotel.get("brief", "No Room Type"),
                            "price": hotel.get("displayPrice", {}).get("price", "No Price"),
                            "image_url": hotel.get("imgUrl", "No Image"),
                        }
                        hotels_data.append(hotel_data)

                        # Yield item for Scrapy pipeline
                        item = ProductItem()
                        item.update(hotel_data)
                        yield item

            # Save filtered hotels data to a JSON file
            self.save_json_to_file(hotels_data, "hotels_data.json")

    def extract_json_data(self, response):
        """
        Extract JSON data embedded in JavaScript using a known variable identifier.
        """
        script = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

        if script:
            try:
                # Extract JSON-like data from the script text
                json_str = script.split("window.IBU_HOTEL=")[1].split("};")[0] + "}"
                json_data = json.loads(json_str)
                return json_data

            except Exception as e:
                self.logger.error(f"Failed to parse JSON from script: {e}")

        return None

    def save_json_to_file(self, data, filename):
        """
        Save the JSON data to a file.
        """
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                self.logger.info(f"JSON data saved to {filename}")
        except Exception as e:
            self.logger.error(f"Failed to save JSON to file: {e}")
