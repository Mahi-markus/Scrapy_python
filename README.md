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
- Python 3.8+ (for local development)
- [Docker](https://www.docker.com/) installed on your system.

---

## Installation and Setup Steps below:

- Clone the repository:

```bash
git clone https://github.com/Mahi-markus/Scrapy_python.git

```

## Create Virtual Environment:

Now open a terminal and run the following commands to create vm.

```bash
python -m venv venv          #On Windows:
venv\Scripts\activate
```

```bash
python3 -m venv venv        #On macOS/Linux:
source venv/bin/activate

```
- Navigate to the project directory:

```bash
cd scrapy_project
```

- Build and start the Docker containers:

```bash
docker-compose up --build
```

This will set up the project and initiate the scraping process.
The scraper will automatically start upon running the docker-compose up --build command. You can monitor the logs to ensure data is being scraped and stored properly.

## Checking the Database

To check the database and view the data in the table, open another terminal and run the following command:

```bash
cd scrapy_project
docker exec -it postgres_db psql -U admin scraper_db
```

Once inside the PostgreSQL shell, use the following SQL query to check the data in the hotels_info table:

```bash
select *from hotels_info;
```

## Testing and Coverage

## Run Tests

Open another terminal and navigate to the project directory:

```bash
cd scrapy_project
```

Then run the following commands:

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

## Termination(Optional):
In order stop and remove the container ,open the specific terminal where docker is running and  run the following commands:

```bash
ctrl c
docker-compose down

```

## Directory Structure:

- **Scrapy Spider (trip_spider.py)**: Handles data scraping from Trip.com.
- **Postgres Database**: Stores scraped property details.
- **Image Directory**: Automatically created to save property images( /images).
- **SQLAlchemy Integration**: Automates table creation and database interaction.
