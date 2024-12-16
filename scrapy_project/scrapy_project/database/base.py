from sqlalchemy import create_engine, Column, String, Integer,Float
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://admin:admin@db:5432/scraper_db"

Base = declarative_base()
engine = create_engine(DATABASE_URL)

class Product(Base):
    __tablename__ = 'hotels7'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Auto-incremented unique ID
    #hotel_id = Column(String, nullable=False)                  # Unique hotel identifier
    title = Column(String, nullable=True)                 # Name of the hotel
    rating = Column(Float, nullable=True)                      # Hotel rating
    location = Column(String, nullable=True)                    # Hotel address
    latitude = Column(Float, nullable=True)                    # Latitude
    longitude = Column(Float, nullable=True)                   # Longitude
    room_type = Column(String, nullable=True)                  # Room type information
    price = Column(String, nullable=True)                      # Price details
    image_path = Column(String, nullable=True)                 # Path to the downloaded image

# Create all tables
Base.metadata.create_all(engine)

