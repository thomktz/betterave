# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install poetry and its dependencies
RUN pip install poetry
RUN poetry config virtualenvs.create false
# Install dependencies but without the development ones
RUN poetry install --no-dev

# Expose port 5000 to be accessible from the outside
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_ENV=production

# Run the init_db script to initialize the database
# and then start the Flask application
CMD poetry run python -m scripts.init_db && python main.py
