import os
import requests
from sqlalchemy.orm import sessionmaker
from scrapy_project.database.base import Product, engine
from scrapy.exceptions import DropItem

class ScrapyProjectPipeline:
    def __init__(self):
        # Initialize database session
        self.Session = sessionmaker(bind=engine)
        self.image_dir = "/images"
        os.makedirs(self.image_dir, exist_ok=True)

    def process_item(self, item, spider):
        # Download and save images
        image_url = item.get('image_url')
        if not image_url:
            raise DropItem(f"Missing image URL for {item['hotel_name']}")

        try:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                image_filename = os.path.join(self.image_dir, os.path.basename(image_url))
                with open(image_filename, 'wb') as f:
                    f.write(response.content)
            else:
                raise DropItem(f"Failed to download image for {item['name']}")

        except requests.RequestException as e:
            raise DropItem(f"Error downloading image for {item['name']}: {str(e)}")

        # Save to database
        try:
            session = self.Session()
            product = Product(
                title=item.get('hotel_name', 'Unknown Hotel'),
                rating=float(item.get('rating', 0)),  # Default rating to 0 if missing
                location=item.get('location', 'Unknown Address'),
                latitude=float(item.get('latitude', 0)),  # Default latitude to 0 if missing
                longitude=float(item.get('longitude', 0)),  # Default longitude to 0 if missing
                room_type=item.get('room_type', 'Unknown Room Type'),
                price=item.get('price', 'Unknown Price'),
                image_path=image_filename
            )
            session.add(product)
            session.commit()
        except Exception as e:
            session.rollback()
            raise DropItem(f"Error saving {item['hotel_name']} to database: {str(e)}")
        finally:
            session.close()

        return item
