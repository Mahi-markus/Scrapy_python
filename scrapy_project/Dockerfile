FROM python:3.9-slim

# Set environment variables to improve performance and logging
ENV PYTHONDONTWRITEBYTECODE 1  # Prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED 1        # Ensure Python output is shown in real-time

# Set the working directory in the container
WORKDIR /app


# Install system dependencies (if required)
# Uncomment if additional tools (e.g., curl) are needed:
# RUN apt-get update && apt-get install -y curl && apt-get clean

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Scrapy project into the container
COPY scrapy_project/ /app/scrapy_project/

# Set the default command to run the Scrapy spider
CMD ["scrapy", "crawl", "trip","python", "-m", "unittest", "test_spider.py","coverage", "run"]
