# Cloning Docker Entities - Carla Example

This tutorial demonstrates how to clone, copy, and replicate Docker containers and images. We'll use a sample application called "Carla" to illustrate various cloning techniques.

## Table of Contents

- [Introduction](#introduction)
- [What is Cloning in Docker?](#what-is-cloning-in-docker)
- [Prerequisites](#prerequisites)
- [Scenario 1: Cloning Docker Images](#scenario-1-cloning-docker-images)
- [Scenario 2: Cloning Running Containers](#scenario-2-cloning-running-containers)
- [Scenario 3: Export and Import Containers](#scenario-3-export-and-import-containers)
- [Scenario 4: Save and Load Images](#scenario-4-save-and-load-images)
- [Scenario 5: Creating Modified Copies](#scenario-5-creating-modified-copies)
- [Best Practices](#best-practices)
- [Common Use Cases](#common-use-cases)

## Introduction

In Docker, "cloning" refers to creating copies of containers, images, or entire environments. This is essential for:
- **Development**: Creating identical environments for team members
- **Testing**: Replicating production environments
- **Backup**: Preserving container states
- **Distribution**: Sharing applications across systems

## What is Cloning in Docker?

Docker doesn't have a direct "clone" command, but offers several methods to achieve cloning:

1. **Image Tagging**: Creating multiple tags for the same image
2. **Container Commit**: Converting containers to images
3. **Export/Import**: Moving containers between systems
4. **Save/Load**: Moving images between systems
5. **Docker Compose**: Replicating entire application stacks

## Prerequisites

- Docker 24.0 or later installed
- Basic understanding of Docker commands (see `1-running-containers`)
- Basic understanding of building images (see `2-building-images`)

## Scenario 1: Cloning Docker Images

The simplest form of cloning is creating new tags for existing images.

### Step 1: Build the Carla Application

First, let's build our sample application:

```bash
cd carla-app
docker build -t carla-app:original .
```

### Step 2: Clone by Creating New Tags

Create multiple tags for the same image:

```bash
# Create a clone with a different tag
docker tag carla-app:original carla-app:clone1

# Create another clone
docker tag carla-app:original carla-app:clone2

# Create a clone with a different repository name
docker tag carla-app:original carla-backup:v1
```

### Step 3: Verify the Clones

```bash
# List all images - you'll see they share the same IMAGE ID
docker images | grep carla
```

**Important**: These aren't true copies; they're references to the same image data. They share disk space!

## Scenario 2: Cloning Running Containers

Sometimes you need to clone a running container with its current state.

### Step 1: Run the Original Container

```bash
docker run -d --name carla-original -p 5000:5000 carla-app:original
```

### Step 2: Make Some Changes

Open your browser to `http://localhost:5000` and interact with the app.

### Step 3: Commit the Container to Create a Clone

```bash
# Commit the container's current state to a new image
docker commit carla-original carla-app:modified

# Now run a clone from this image
docker run -d --name carla-clone -p 5001:5000 carla-app:modified
```

The clone now runs on port 5001 with the same state as the original!

## Scenario 3: Export and Import Containers

Use this method to move containers between machines or create backups.

### Step 1: Export a Container

```bash
# Export the container filesystem
docker export carla-original > carla-container.tar

# Check the file size
ls -lh carla-container.tar
```

### Step 2: Import on Another System (or the Same)

```bash
# Import the tarball as a new image
cat carla-container.tar | docker import - carla-app:imported

# Run a container from the imported image
docker run -d --name carla-imported -p 5002:5000 carla-app:imported python app.py
```

**Note**: You need to specify the command (`python app.py`) because import doesn't preserve CMD/ENTRYPOINT.

## Scenario 4: Save and Load Images

This method preserves all image metadata (layers, history, tags).

### Step 1: Save an Image

```bash
# Save the image to a tar file
docker save carla-app:original -o carla-image.tar

# Or compress it
docker save carla-app:original | gzip > carla-image.tar.gz
```

### Step 2: Load on Another System

```bash
# Load the image
docker load -i carla-image.tar

# Or from compressed file
gunzip -c carla-image.tar.gz | docker load

# Verify
docker images | grep carla
```

**Difference from Export/Import**:
- `save/load`: Preserves layers, history, and metadata
- `export/import`: Creates a flattened filesystem (single layer)

## Scenario 5: Creating Modified Copies

Create clones with modifications using Dockerfile inheritance.

### Step 1: Create a Derivative Dockerfile

Create `Dockerfile.clone`:

```dockerfile
# Start from the original Carla app
FROM carla-app:original

# Add modifications
ENV APP_MODE=clone
LABEL version="clone-1"
LABEL description="Modified clone of Carla application"

# Add a clone identifier file
RUN echo "This is a clone" > /app/clone-marker.txt
```

### Step 2: Build the Clone

```bash
docker build -f Dockerfile.clone -t carla-app:custom-clone .
```

### Step 3: Run Both and Compare

```bash
# Run original
docker run -d --name carla-original -p 5000:5000 carla-app:original

# Run clone
docker run -d --name carla-custom-clone -p 5003:5000 carla-app:custom-clone

# Compare
docker exec carla-original cat /app/clone-marker.txt 2>/dev/null || echo "File not found in original"
docker exec carla-custom-clone cat /app/clone-marker.txt
```

## Best Practices

### 1. Use Meaningful Tags

```bash
# Good
docker tag app:v1.0 app:production-backup-2025-01-13

# Not so good
docker tag app:v1.0 app:backup
```

### 2. Document Clone Purpose

Use labels to track clones:

```dockerfile
LABEL clone.source="carla-app:original"
LABEL clone.date="2025-01-13"
LABEL clone.reason="testing"
```

### 3. Clean Up Unused Clones

```bash
# Remove unused images
docker image prune -a

# Remove specific clones
docker rmi carla-app:clone1 carla-app:clone2
```

### 4. Use Docker Compose for Complex Cloning

For multi-container applications, use Docker Compose:

```bash
# Clone an entire stack
docker compose -f docker-compose.yml -p carla-original up -d
docker compose -f docker-compose.yml -p carla-clone up -d
```

### 5. Version Your Clones

```bash
docker tag carla-app:original carla-app:backup-$(date +%Y%m%d-%H%M%S)
```

## Common Use Cases

### Use Case 1: Team Development

Each developer gets an identical environment:

```bash
# Team lead creates the image
docker save team-env:v1.0 | gzip > team-env.tar.gz

# Team members load it
gunzip -c team-env.tar.gz | docker load
docker run -d --name my-env team-env:v1.0
```

### Use Case 2: Blue-Green Deployment

Run old and new versions simultaneously:

```bash
# Blue (current production)
docker run -d --name app-blue -p 8080:5000 carla-app:v1.0

# Green (new version)
docker run -d --name app-green -p 8081:5000 carla-app:v2.0

# Test green, then swap ports
```

### Use Case 3: Testing Different Configurations

```bash
# Original with default config
docker run -d --name carla-default carla-app:original

# Clone with custom config
docker run -d --name carla-custom -v $(pwd)/custom-config:/app/config carla-app:original

# Clone with different environment
docker run -d --name carla-debug -e DEBUG=true carla-app:original
```

### Use Case 4: Disaster Recovery

Regular backups:

```bash
#!/bin/bash
# backup-script.sh
DATE=$(date +%Y%m%d)
docker save carla-app:original | gzip > backups/carla-$DATE.tar.gz
docker export carla-running > backups/carla-state-$DATE.tar
```

## Summary

### Quick Reference

| Goal | Command |
|------|---------|
| Clone image (tag) | `docker tag source:tag destination:tag` |
| Clone container state | `docker commit container new-image:tag` |
| Export container | `docker export container > file.tar` |
| Import container | `cat file.tar \| docker import - image:tag` |
| Save image | `docker save image:tag > file.tar` |
| Load image | `docker load -i file.tar` |
| Clone with modifications | Create new Dockerfile using `FROM` |

### When to Use Each Method

- **Tag**: Quick references, no disk overhead
- **Commit**: Preserve runtime changes
- **Export/Import**: Move containers, flatten layers
- **Save/Load**: Move images, preserve metadata
- **Dockerfile FROM**: Create modified variants

## Next Steps

- Learn about `docker-compose` for multi-container cloning: `../1-5-running-docker-compose`
- Explore Docker Swarm for production-scale cloning: `../5-docker-swarm`
- Check out the Docker Cheatsheet: `../docker-cheatsheet.md`

---

## Clean Up

After completing this tutorial:

```bash
# Stop all Carla containers
docker stop $(docker ps -a | grep carla | awk '{print $1}')

# Remove all Carla containers
docker rm $(docker ps -a | grep carla | awk '{print $1}')

# Remove all Carla images
docker rmi $(docker images | grep carla | awk '{print $3}')

# Remove exported files
rm -f carla-container.tar carla-image.tar carla-image.tar.gz
```

---

**Congratulations!** You now understand how to clone Docker entities effectively. This skill is crucial for development, testing, and production workflows.
