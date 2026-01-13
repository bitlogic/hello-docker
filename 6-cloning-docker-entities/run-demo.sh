#!/bin/bash

# Demo script for Docker cloning techniques
# Part of the Carla cloning tutorial

set -e  # Exit on error

echo "╔════════════════════════════════════════════╗"
echo "║  Carla Docker Cloning Demo Script         ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print step
print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print info
print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

cd "$(dirname "$0")/carla-app"

print_step "Step 1: Building the original Carla application..."
docker build -t carla-app:original .
print_success "Original image built successfully!"
echo ""

print_step "Step 2: Running the original container..."
docker run -d --name carla-original -p 5000:5000 carla-app:original
print_success "Original container running on http://localhost:5000"
echo ""

sleep 2

print_step "Step 3: Creating clones using different methods..."
echo ""

print_info "Method 1: Clone by tagging (shares same image)"
docker tag carla-app:original carla-app:clone-by-tag
print_success "Clone created: carla-app:clone-by-tag"
echo ""

print_info "Method 2: Clone by committing running container"
docker commit carla-original carla-app:clone-by-commit
print_success "Clone created: carla-app:clone-by-commit"
echo ""

print_info "Method 3: Clone by building with different Dockerfile"
docker build -f carla-app/Dockerfile.clone -t carla-app:clone-by-build .
print_success "Clone created: carla-app:clone-by-build"
echo ""

print_step "Step 4: Running clone containers..."
docker run -d --name carla-clone-1 -p 5001:5000 carla-app:clone-by-commit
print_success "Clone 1 running on http://localhost:5001"

docker run -d --name carla-clone-2 -p 5002:5000 carla-app:clone-by-build
print_success "Clone 2 running on http://localhost:5002"
echo ""

print_step "Step 5: Comparing images..."
echo ""
docker images | grep carla
echo ""

print_step "Step 6: Showing container information..."
echo ""
docker ps | grep carla
echo ""

print_info "Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Original:  http://localhost:5000"
echo "Clone 1:   http://localhost:5001"
echo "Clone 2:   http://localhost:5002"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Visit these URLs in your browser to see the different instances!"
echo ""
echo "To clean up, run: ./cleanup-demo.sh"
