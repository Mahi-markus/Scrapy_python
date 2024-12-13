from sqlalchemy import create_engine, Column, String, Integer,Float
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://admin:admin@db:5432/scraper_db"

Base = declarative_base()
engine = create_engine(DATABASE_URL)

class Product(Base):
    __tablename__ = 'products1'
    id = Column(Integer, primary_key=True, autoincrement=True,nullable=True)
    name = Column(String, nullable=True)          # Property title
    rating = Column(Float, nullable=True)          # Property rating
    location = Column(String, nullable=True)       # Property location
    latitude = Column(Float, nullable=True)        # Geospatial latitude
    longitude = Column(Float, nullable=True)       # Geospatial longitude
    room_type = Column(String, nullable=True)      # Room type
    price = Column(String, nullable=True)         # Price details
    image_path = Column(String, nullable=True)    # Path to the image file
    url = Column(String, nullable=True)           # URL to the property page

# Create all tables
Base.metadata.create_all(engine)

