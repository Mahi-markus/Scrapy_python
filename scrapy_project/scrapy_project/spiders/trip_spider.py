import scrapy
import json
import re
import random


class TripHotelsSpider(scrapy.Spider):
    name = "trip"
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
        # Extract the script containing the JSON object
        script_data = response.xpath(
            '//script[contains(text(), "window.IBU_HOTEL")]/text()'
        ).get()

        if not script_data:
            self.logger.error("No script containing 'window.IBU_HOTEL' found on the main page!")
            return

        # Extract JSON structure using regex
        match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script_data, re.DOTALL)

        if match:
            try:
                # Parse JSON data
                json_data = match.group(1)
                data = json.loads(json_data)

                # Print the JSON structure for debugging
                self.logger.info("Extracted JSON data: %s", json.dumps(data, indent=2))

                # Extract inboundCities and outboundCities
                inbound_cities = data.get("initData", {}).get("htlsData", {}).get("inboundCities", [])
                outbound_cities = data.get("initData", {}).get("htlsData", {}).get("outboundCities", [])

                # Ensure both lists exist
                if not inbound_cities and not outbound_cities:
                    self.logger.error("No inbound or outbound cities found in the JSON data!")
                    return

                # Randomly choose between inboundCities and outboundCities
                chosen_city_list = random.choice([inbound_cities, outbound_cities])

                # Select a random city
                random_city = random.choice(chosen_city_list)
                city_id = random_city.get("id")
                city_name = random_city.get("name")

                if not city_id:
                    self.logger.error(f"City ID is missing for city: {city_name}")
                    return

                # Construct the URL for the city
                hotels_list_url = f"https://uk.trip.com/hotels/list?city={city_id}"

                # Pass city ID and name to the next parsing function
                yield scrapy.Request(
                    hotels_list_url,
                    callback=self.parse_city_hotels,
                    meta={"city_id": city_id, "city_name": city_name}
                )

            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to decode JSON: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error occurred: {e}")
        else:
            self.logger.error("Could not match the window.IBU_HOTEL object in the script.")

    def parse_city_hotels(self, response):
        # Extract script containing JSON on the city hotels page
        script_data = response.xpath(
            '//script[contains(text(), "window.IBU_HOTEL")]/text()'
        ).get()

        if not script_data:
            self.logger.error("No script containing 'window.IBU_HOTEL' found on the city hotels page!")
            return

        # Extract JSON structure using regex
        match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script_data, re.DOTALL)

        if match:
            try:
                # Parse JSON data
                json_data = match.group(1)
                data = json.loads(json_data)

                # Print the JSON structure for debugging
                self.logger.info("Extracted JSON data from city hotels: %s", json.dumps(data, indent=2))

                # Extract hotel list from the JSON data
                hotel_list = data.get("initData", {}).get("firstPageList", {}).get("hotelList", [])

                if not hotel_list:
                    self.logger.error("No hotels found in the JSON data for the city!")
                    return

                # Get city ID and name from meta
                city_id = response.meta.get("city_id")
                city_name = response.meta.get("city_name")

                # Iterate through each hotel and extract required details
                for hotel in hotel_list:
                    hotel_basic_info = hotel.get("hotelBasicInfo", {})
                    comment_info = hotel.get("commentInfo", {})
                    room_info = hotel.get("roomInfo", {})
                    position_info = hotel.get("positionInfo", {})
                    coordinate = position_info.get("coordinate", {})

                    # Extract hotel details
                    hotel_data = {
                        "city_id": city_id,
                        "city_name": city_name,
                        "hotel_id": hotel_basic_info.get("hotelId"),
                        "hotel_name": hotel_basic_info.get("hotelName"),
                        "rating": comment_info.get("commentScore"),
                        "address": position_info.get("positionName"),
                        "latitude": coordinate.get("lat"),
                        "longitude": coordinate.get("lng"),
                        "room_type": room_info.get("physicalRoomName"),
                        "price": hotel_basic_info.get("price"),
                        "image_url": hotel_basic_info.get("hotelImg"),
                    }

                    # Log the hotel data for debugging
                    self.logger.info("Extracted hotel data: %s", json.dumps(hotel_data, indent=2))

                    # Yield hotel data for further processing or saving
                    if any(hotel_data.values()):  # Ensure at least one field has data
                        yield hotel_data

            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to decode JSON: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error occurred: {e}")
        else:
            self.logger.error("Could not match the window.IBU_HOTEL object in the script.")
