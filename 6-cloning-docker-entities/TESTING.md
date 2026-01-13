# Testing Guide for Docker Cloning Tutorial

This guide helps you verify that the Carla cloning tutorial works correctly.

## Prerequisites

Before testing, ensure:
- Docker daemon is running: `docker ps`
- You have sufficient disk space (at least 2GB free)
- No other services are using ports 5000-5003

## Quick Test

### 1. Basic Build Test

```bash
cd 6-cloning-docker-entities/carla-app
docker build -t carla-app:test .
```

**Expected output**: Image builds successfully without errors

### 2. Run Single Instance

```bash
docker run -d --name carla-test -p 5000:5000 carla-app:test
```

**Expected output**: Container ID returned

### 3. Verify Application

```bash
# Check container is running
docker ps | grep carla-test

# Check health
curl http://localhost:5000/health

# Open in browser
open http://localhost:5000  # macOS
# or
xdg-open http://localhost:5000  # Linux
```

**Expected output**: 
- Container appears in `docker ps`
- Health endpoint returns JSON with `{"status":"healthy",...}`
- Browser shows beautiful Carla application

### 4. Test Cloning Operations

```bash
# Test image tagging
docker tag carla-app:test carla-app:clone1
docker images | grep carla

# Test container commit
docker commit carla-test carla-app:committed
docker images | grep carla

# Test export
docker export carla-test > test-export.tar
ls -lh test-export.tar
```

**Expected output**: All commands succeed without errors

### 5. Clean Up Test

```bash
docker stop carla-test
docker rm carla-test
docker rmi carla-app:test carla-app:clone1 carla-app:committed
rm test-export.tar
```

## Full Demo Test

Run the automated demo script:

```bash
cd 6-cloning-docker-entities
./run-demo.sh
```

**Expected output**:
- Script builds images
- Runs 3 containers (original + 2 clones)
- Shows summary with URLs
- All containers accessible on different ports

**Verify**:
```bash
# Check all containers are running
docker ps | grep carla

# Test all endpoints
curl http://localhost:5000/health
curl http://localhost:5001/health
curl http://localhost:5002/health
```

**Clean up**:
```bash
./cleanup-demo.sh
```

## Docker Compose Test

```bash
cd carla-app
docker compose up -d
```

**Expected output**: 
- 3 services start successfully
- carla-original on port 5000
- carla-clone-1 on port 5001
- carla-clone-2 on port 5002

**Verify**:
```bash
docker compose ps
curl http://localhost:5000/stats
curl http://localhost:5001/stats
curl http://localhost:5002/stats
```

**Check differences**:
- Port 5000 should show `"mode":"original"`
- Port 5001 should show `"mode":"clone"`
- Port 5002 should show `"mode":"clone"`

**Clean up**:
```bash
docker compose down --rmi all
```

## Advanced Test Cases

### Test 1: Export and Import

```bash
cd carla-app
docker build -t carla-app:export-test .
docker run -d --name carla-export -p 5000:5000 carla-app:export-test

# Make some state changes (visit the app, send messages)

# Export
docker export carla-export > carla-export.tar

# Import
cat carla-export.tar | docker import - carla-app:imported

# Run imported
docker run -d --name carla-imported -p 5001:5000 carla-app:imported python app.py

# Verify both work
curl http://localhost:5000/health
curl http://localhost:5001/health
```

### Test 2: Save and Load

```bash
# Save
docker save carla-app:export-test | gzip > carla-save.tar.gz

# Remove image
docker rmi carla-app:export-test

# Load
gunzip -c carla-save.tar.gz | docker load

# Verify
docker images | grep carla
```

### Test 3: Clone with Modifications

```bash
cd carla-app
docker build -f Dockerfile.clone -t carla-app:custom .

# Run both versions
docker run -d --name carla-original -p 5000:5000 carla-app:export-test
docker run -d --name carla-custom -p 5001:5000 carla-app:custom

# Check differences
docker exec carla-original cat /app/build-info.txt
docker exec carla-custom cat /app/build-info.txt
docker exec carla-custom cat /app/clone-marker.txt

# Check environment
curl http://localhost:5000/stats  # Should show mode: original
curl http://localhost:5001/stats  # Should show mode: clone
```

## Troubleshooting

### Port Already in Use

```bash
# Find what's using the port
lsof -i :5000
# or
netstat -tulpn | grep 5000

# Kill the process or use different ports
docker run -d --name carla-test -p 5010:5000 carla-app:test
```

### Docker Daemon Not Running

```bash
# Check status
systemctl status docker  # Linux
# or
docker info

# Start daemon
sudo systemctl start docker  # Linux
# or open Docker Desktop on macOS/Windows
```

### Build Fails

```bash
# Check Docker version
docker --version

# Clean build cache
docker builder prune -a

# Rebuild with no cache
docker build --no-cache -t carla-app:test .
```

### Container Crashes

```bash
# Check logs
docker logs carla-test

# Check container status
docker ps -a | grep carla

# Inspect container
docker inspect carla-test
```

## Validation Checklist

- [ ] README.md is clear and comprehensive
- [ ] Application builds without errors
- [ ] Container runs and is accessible
- [ ] Health endpoint responds correctly
- [ ] UI loads properly in browser
- [ ] All cloning methods work (tag, commit, export, save)
- [ ] Docker Compose starts all services
- [ ] Different modes are visible (original vs clone)
- [ ] Demo script runs without errors
- [ ] Cleanup script removes all resources
- [ ] No sensitive data in images
- [ ] Images are reasonably sized (< 500MB)

## Performance Benchmarks

Expected metrics:
- Build time: 30-60 seconds
- Image size: 150-200 MB
- Container start time: < 5 seconds
- Health check response: < 100ms
- Memory usage per container: ~50MB

## Integration Tests

### Test API Endpoints

```bash
# Health
curl -X GET http://localhost:5000/health

# Visit
curl -X POST http://localhost:5000/visit

# Message
curl -X POST http://localhost:5000/message \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","message":"Hello"}'

# Stats
curl -X GET http://localhost:5000/stats
```

**Expected**: All endpoints return valid JSON responses

## Documentation Review

- [ ] README explains purpose clearly
- [ ] All commands are tested and work
- [ ] Prerequisites are listed
- [ ] Examples are correct
- [ ] Cleanup instructions provided
- [ ] Best practices included
- [ ] Use cases make sense
- [ ] Links to other tutorials work

## Final Verification

After all tests pass:

```bash
# Ensure everything is cleaned up
docker ps -a | grep carla  # Should return nothing
docker images | grep carla  # Should return nothing

# Final cleanup
docker system prune -a --volumes
```

---

**Test Status**: ✅ All tests should pass for production-ready tutorial

If any test fails, review the relevant section and fix before merging.
