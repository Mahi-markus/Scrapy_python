import scrapy
import json
import re
import random


class TripHotelsSpider(scrapy.Spider):
    name = "trip"
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
        # Locate the script containing hotel data on the main page
        script_content = response.xpath(
            '//script[contains(text(), "window.IBU_HOTEL")]/text()'
        ).get()

        if not script_content:
            self.logger.error("Failed to locate script with 'window.IBU_HOTEL' on the main page.")
            return

        # Extract JSON data using a regex pattern
        json_match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script_content, re.DOTALL)

        if json_match:
            try:
                # Parse the extracted JSON string
                raw_json = json_match.group(1)
                hotel_data = json.loads(raw_json)

                self.logger.debug("Successfully extracted hotel JSON data.")

                # Retrieve city data (inbound and outbound)
                htls_data = hotel_data.get("initData", {}).get("htlsData", {})
                inbound_cities = htls_data.get("inboundCities", [])
                outbound_cities = htls_data.get("outboundCities", [])

                # Verify availability of city data
                if not inbound_cities and not outbound_cities:
                    self.logger.warning("No inbound or outbound cities found in the data.")
                    return

                # Choose between inbound and outbound cities randomly
                city_options = random.choice([inbound_cities, outbound_cities])
                selected_city = random.choice(city_options)
                city_id = selected_city.get("id")
                city_name = selected_city.get("name")

                if not city_id:
                    self.logger.warning(f"City ID missing for selected city: {city_name}")
                    return

                # Construct URL for hotels in the selected city
                hotels_url = f"https://uk.trip.com/hotels/list?city={city_id}"

                # Trigger next parsing stage for city hotels
                yield scrapy.Request(
                    hotels_url,
                    callback=self.parse_city_hotels,
                    meta={"city_id": city_id, "city_name": city_name}
                )

            except json.JSONDecodeError as e:
                self.logger.error(f"JSON decoding error: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error during main page parsing: {e}")
        else:
            self.logger.error("Failed to extract 'window.IBU_HOTEL' JSON data from the script.")

    def parse_city_hotels(self, response):
        # Locate the script containing hotel data on the city-specific hotels page
        script_content = response.xpath(
            '//script[contains(text(), "window.IBU_HOTEL")]/text()'
        ).get()

        if not script_content:
            self.logger.error("Failed to locate script with 'window.IBU_HOTEL' on the city hotels page.")
            return

        # Extract JSON data using a regex pattern
        json_match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script_content, re.DOTALL)

        if json_match:
            try:
                # Parse the extracted JSON string
                raw_json = json_match.group(1)
                hotel_data = json.loads(raw_json)

                self.logger.debug("Successfully extracted JSON data from city hotels page.")

                # Retrieve hotel list
                hotel_list = hotel_data.get("initData", {}).get("firstPageList", {}).get("hotelList", [])

                if not hotel_list:
                    self.logger.warning("No hotels found in the JSON data for the city.")
                    return

                # Retrieve city details from meta
                # city_id = response.meta.get("city_id")
                # city_name = response.meta.get("city_name")

                # Iterate through each hotel and extract details
                for hotel in hotel_list:
                    basic_info = hotel.get("hotelBasicInfo", {})
                    comments = hotel.get("commentInfo", {})
                    position = hotel.get("positionInfo", {}).get("coordinate", {})
                    room_info = hotel.get("roomInfo", {})

                    # Structure extracted data
                    hotel_details = {
                        "title": basic_info.get("hotelName"),
                        "rating": comments.get("commentScore"),
                        "location": hotel.get("positionInfo", {}).get("positionName"),
                        "latitude": position.get("lat"),
                        "longitude": position.get("lng"),
                        "room_type": room_info.get("physicalRoomName"),
                        "price": basic_info.get("price"),
                        "image_url": basic_info.get("hotelImg"),
                    }

                    # Log hotel details for review
                    self.logger.debug(f"Extracted hotel details: {hotel_details}")

                    # Yield hotel data for processing
                    if any(hotel_details.values()):
                        yield hotel_details

            except json.JSONDecodeError as e:
                self.logger.error(f"JSON decoding error: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error during city hotels parsing: {e}")
        else:
            self.logger.error("Failed to extract 'window.IBU_HOTEL' JSON data from the script.")

