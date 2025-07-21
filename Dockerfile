# Use official Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8080

# Set env variable for gunicorn
ENV PORT 8080

# Start the app using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
