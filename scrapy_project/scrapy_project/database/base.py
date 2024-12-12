from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://admin:admin@db:5432/scraper_db"

Base = declarative_base()
engine = create_engine(DATABASE_URL)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(String, nullable=False)
    url = Column(String, nullable=False)
    image_path = Column(String, nullable=False)

# Create all tables
Base.metadata.create_all(engine)

