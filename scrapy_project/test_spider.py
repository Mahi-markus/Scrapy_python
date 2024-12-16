import unittest
from unittest.mock import patch
from scrapy.http import HtmlResponse, Request
from scrapy_project.spiders.trip_spider import TripHotelsSpider


class TestTripHotelsSpider(unittest.TestCase):

    @patch('scrapy_project.spiders.trip_spider.TripHotelsSpider.parse_city_hotels')
    @patch('random.choice', side_effect=lambda x: x[0])  # Mock `random.choice` to always pick the first option
    def test_parse_main_page(self, mock_random_choice, mock_parse_city_hotels):
        # Mock response for the main page
        body = '''
        <html>
            <script>
                window.IBU_HOTEL = {
                    "initData": {
                        "htlsData": {
                            "inboundCities": [
                                {"id": "123", "name": "CityA"}
                            ],
                            "outboundCities": [
                                {"id": "456", "name": "CityB"}
                            ]
                        }
                    }
                };
            </script>
        </html>
        '''
        response = HtmlResponse(url='https://uk.trip.com/hotels/', body=body, encoding='utf-8')

        spider = TripHotelsSpider()

        # Mock Scrapy Request
        with patch('scrapy.Request', wraps=Request) as mock_request:
            result = list(spider.parse(response))

            # Extract expected city data
            expected_city_id = "123"
            expected_city_name = "CityA"
            expected_url = f'https://uk.trip.com/hotels/list?city={expected_city_id}'

            # Verify the correct request was made
            mock_request.assert_called_with(
                expected_url,
                callback=mock_parse_city_hotels,
                meta={"city_id": expected_city_id, "city_name": expected_city_name},
            )
            self.assertEqual(len(result), 1)  # Ensure one request was yielded

    def test_parse_city_hotels(self):
        # Mock response for the city hotels page
        body = '''
        <html>
            <script>
                window.IBU_HOTEL = {
                    "initData": {
                        "firstPageList": {
                            "hotelList": [
                                {
                                    "hotelBasicInfo": {
                                        "hotelName": "HotelA",
                                        "price": "200",
                                        "hotelImg": "https://example.com/image.jpg"
                                    },
                                    "commentInfo": {
                                        "commentScore": 4.8
                                    },
                                    "positionInfo": {
                                        "positionName": "City Center",
                                        "coordinate": {"lat": 52.2053, "lng": 0.1218}
                                    },
                                    "roomInfo": {
                                        "physicalRoomName": "Suite"
                                    }
                                }
                            ]
                        }
                    }
                };
            </script>
        </html>
        '''
        # Mock the request with meta data
        mock_request = Request(
            url='https://uk.trip.com/hotels/list?city=123',
            meta={"city_id": "123", "city_name": "CityA"}
        )
        response = HtmlResponse(
            url='https://uk.trip.com/hotels/list?city=123',
            body=body,
            encoding='utf-8',
            request=mock_request,
        )

        spider = TripHotelsSpider()
        result = list(spider.parse_city_hotels(response))

        # Define the expected hotel data
        expected_hotel = {
            "title": "HotelA",
            "rating": 4.8,
            "location": "City Center",
            "latitude": 52.2053,
            "longitude": 0.1218,
            "room_type": "Suite",
            "price": "200",
            "image_url": "https://example.com/image.jpg",
        }

        self.assertEqual(len(result), 1)  # Ensure one hotel was yielded
        self.assertEqual(result[0], expected_hotel)


if __name__ == '__main__':
    unittest.main()
