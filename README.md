# Trip.com Property Scraper

This project is a Scrapy-based web scraper for extracting property information from [Trip.com](https://uk.trip.com/hotels/?locale=en-GB&curr=GBP) and storing the data in a PostgreSQL database using SQLAlchemy. The system is designed to dynamically gather property data and save it for future use.

---

## Features

- Scrapes property details like title, rating, location, latitude, longitude, room type, price, and images.
- Stores scraped data in a PostgreSQL database.
- Saves images in a directory and references them in the database.
- Automatically creates database tables and directory structures.
- Provides robust testing and coverage reporting.

---

## Prerequisites

- [Docker](https://www.docker.com/) installed on your system.

---

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/Mahi-markus/Scrapy_python.git
```

2. Navigate to the project directory:

```bash
cd scrapy_project
```

3. Build and start the Docker containers:

```bash
docker-compose up --build
```

This will set up the project and initiate the scraping process.
The scraper will automatically start upon running the docker-compose up --build command. You can monitor the logs to ensure data is being scraped and stored properly.

## Testing and Coverage

## Run Tests

Open another terminal and navigate to the project directory:

```bash
cd scrapy_project
```

Then run:

```bash
docker-compose run --rm scrapy python -m unittest discover
```

Run Coverage:

```bash
docker-compose run --rm scrapy coverage run -m unittest discover
```

Generate Test Report

```bash
docker-compose run --rm scrapy coverage report
```

Directory Structure:

- Scrapy Spider: Handles data scraping from Trip.com.
- Postgres Database: Stores scraped property details.
- Image Directory: Automatically created to save property images.
- SQLAlchemy Integration: Automates table creation and database interaction.
