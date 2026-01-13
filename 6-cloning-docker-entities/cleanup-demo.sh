#!/bin/bash

# Cleanup script for Carla cloning demo
# Removes all containers, images, and files created during the demo

echo "╔════════════════════════════════════════════╗"
echo "║  Carla Docker Cloning Demo - Cleanup      ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_action() {
    echo -e "${YELLOW}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${RED}! $1${NC}"
}

# Stop and remove containers
print_action "Stopping Carla containers..."
docker stop carla-original carla-clone-1 carla-clone-2 2>/dev/null || true
docker stop $(docker ps -a | grep carla | awk '{print $1}') 2>/dev/null || true
print_success "Containers stopped"

print_action "Removing Carla containers..."
docker rm carla-original carla-clone-1 carla-clone-2 2>/dev/null || true
docker rm $(docker ps -a | grep carla | awk '{print $1}') 2>/dev/null || true
print_success "Containers removed"

# Remove images
print_action "Removing Carla images..."
docker rmi carla-app:original 2>/dev/null || true
docker rmi carla-app:clone-by-tag 2>/dev/null || true
docker rmi carla-app:clone-by-commit 2>/dev/null || true
docker rmi carla-app:clone-by-build 2>/dev/null || true
docker rmi carla-app:clone 2>/dev/null || true
docker rmi carla-app:modified 2>/dev/null || true
docker rmi carla-app:imported 2>/dev/null || true
docker rmi carla-app:custom-clone 2>/dev/null || true
docker rmi carla-backup:v1 2>/dev/null || true
docker rmi $(docker images | grep carla | awk '{print $3}') 2>/dev/null || true
print_success "Images removed"

# Remove exported files
print_action "Removing exported files..."
cd "$(dirname "$0")"
rm -f carla-container.tar carla-image.tar carla-image.tar.gz 2>/dev/null || true
rm -f carla-app/carla-container.tar carla-app/carla-image.tar carla-app/carla-image.tar.gz 2>/dev/null || true
print_success "Exported files removed"

# Docker compose cleanup
print_action "Cleaning up Docker Compose resources..."
cd carla-app
docker compose down --rmi all --volumes 2>/dev/null || true
cd ..
print_success "Docker Compose resources cleaned"

# Show remaining Docker resources
echo ""
echo "Remaining Docker resources:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Images with 'carla':"
docker images | grep carla || echo "  (none)"
echo ""
echo "Containers with 'carla':"
docker ps -a | grep carla || echo "  (none)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
print_success "Cleanup complete!"
