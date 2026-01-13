# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Create a non-root user to run the application
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy the app code and dependencies file into the container at /app
# Use COPY instead of ADD for better transparency (security best practice)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appuser /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME=World

# Switch to non-root user
USER appuser

# Run app.py when the container launches
CMD ["python", "app.py"]