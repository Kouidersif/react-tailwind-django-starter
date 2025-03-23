# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/backend
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the Django project files
COPY . /app/backend

# copy entrypoint.sh
COPY ./entrypoints.sh /app/backend/

RUN sed -i 's/\r$//g' /app/backend/entrypoints.sh
RUN chmod +x /app/backend/entrypoints.sh

# Run the Django development server
CMD ["/app/backend/entrypoints.sh"]