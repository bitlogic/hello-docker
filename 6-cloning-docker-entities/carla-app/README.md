# Carla Application

A simple Flask web application designed to demonstrate Docker cloning techniques.

## Features

- 👋 Welcome page with visitor tracking
- 💬 Message board functionality
- 📊 Application statistics
- 🏥 Health check endpoint
- 🎨 Beautiful, modern UI

## Quick Start

### Option 1: Build and Run Manually

```bash
# Build the original image
docker build -t carla-app:original .

# Run the container
docker run -d --name carla-original -p 5000:5000 carla-app:original

# Access the application
open http://localhost:5000
```

### Option 2: Use Docker Compose

```bash
# Start all services (original + 2 clones)
docker compose up -d

# Access the services
# Original: http://localhost:5000
# Clone 1:  http://localhost:5001
# Clone 2:  http://localhost:5002
```

## Building Clone Versions

```bash
# Build a clone with the clone Dockerfile
docker build -f Dockerfile.clone -t carla-app:clone .

# Or create a clone by tagging
docker tag carla-app:original carla-app:clone

# Or commit a running container
docker commit carla-original carla-app:modified
```

## Environment Variables

- `APP_MODE`: Set to `original` or `clone` (default: `original`)
- `VERSION`: Application version number (default: `1.0`)

## API Endpoints

- `GET /` - Main application page
- `POST /visit` - Record a visitor
- `POST /message` - Submit a message
- `GET /stats` - View application statistics
- `GET /health` - Health check endpoint

## Clean Up

```bash
# Stop and remove containers
docker compose down

# Remove images
docker rmi carla-app:original carla-app:clone

# Or clean everything
docker compose down --rmi all --volumes
```

## Tutorial Reference

This application is part of the Docker cloning tutorial. See the main README.md in the parent directory for detailed cloning techniques.
