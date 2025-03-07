# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn 

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable to ensure Python output is sent directly to terminal
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "main.py"]