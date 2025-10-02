# Docker for Dummies: A Beginner's Guide

## What is Docker?

Docker is a platform that allows you to package applications and their dependencies into lightweight, portable containers. Think of containers as standardized shipping boxes for your code - they contain everything needed to run your application, regardless of the environment.

### 🛠️ Key Concepts
| Term         | Description |
|--------------|-------------|
| **Image**    | A snapshot of your app and its environment. |
| **Container**| A running instance of an image. |
| **Dockerfile**| A script to build a Docker image. |
| **Docker Hub**| A public registry for sharing images. |


## Creating Your First Dockerfile

Here's a simple Python application example:

### 1. Create your application
```python
# app.py
print("Hello from Docker!") 
```

### 2. Create a Dockerfile
```dockerfile
# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application file
COPY app.py .

# Run the application
CMD ["python", "app.py"]
```

### 3. Build and run
```bash
# Build the image
docker build -t my-python-app .

# Run the container
docker run my-python-app
```


## Basic Docker Commands

### Getting Started
```bash
# Check Docker version
docker --version

# Pull an image from Docker Hub
docker pull ubuntu

# List downloaded images
docker images

# Run a container
docker run ubuntu echo "Hello Docker!"

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a
```

### Working with Containers
```bash
# Run container interactively
docker run -it ubuntu bash

# Run container in background (detached)
docker run -d nginx

# Stop a running container
docker stop <container_id>

# Remove a container
docker rm <container_id>

# Remove an image
docker rmi <image_name>
```

## 📋 Dockerfile Instructions Explained

A Dockerfile is a script containing a series of instructions that Docker uses to build an image. Each instruction creates a new layer in the image.

### Essential Instructions

#### 🏗️ FROM - Base Image
```dockerfile
FROM python:3.11-slim
FROM ubuntu:20.04
FROM node:16-alpine
```
- **Purpose**: Specifies the base image to start from
- **Must be**: The first instruction in any Dockerfile
- **Best Practice**: Use specific tags instead of `latest`
- **Example**: `FROM python:3.11-slim` uses a lightweight Python 3.11 image

#### 📁 WORKDIR - Set Working Directory
```dockerfile
WORKDIR /app
WORKDIR /usr/src/app
```
- **Purpose**: Sets the working directory for subsequent instructions
- **Creates**: The directory if it doesn't exist
- **Affects**: All following `RUN`, `CMD`, `COPY`, `ADD` instructions
- **Example**: `WORKDIR /app` means all operations happen in `/app`

#### 📋 COPY vs ADD - File Operations
```dockerfile
# COPY - Simple file copying (recommended)
COPY app.py .
COPY requirements.txt ./
COPY src/ /app/src/

# ADD - Advanced copying (use sparingly)
ADD https://example.com/file.tar.gz /app/
ADD archive.tar.gz /app/  # Automatically extracts
```
- **COPY**: Simple, predictable file copying from host to container
- **ADD**: Has extra features (URL downloads, auto-extraction) but less predictable
- **Best Practice**: Use COPY unless you specifically need ADD's features

#### ⚡ RUN - Execute Commands
```dockerfile
# Single command
RUN pip install flask

# Multiple commands (recommended for efficiency)
RUN apt-get update && \
    apt-get install -y curl wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Using uv for faster Python package management
RUN pip install uv && \
    uv venv && \
    uv pip install -r requirements.txt
```
- **Purpose**: Executes commands during image build
- **Creates**: A new layer for each RUN instruction
- **Best Practice**: Chain commands with `&&` to minimize layers

#### 🌍 ENV - Environment Variables
```dockerfile
ENV NODE_ENV=production
ENV PYTHONPATH=/app
ENV DATABASE_URL=postgresql://localhost/mydb
ENV PATH="/app/bin:${PATH}"
```
- **Purpose**: Sets environment variables available during build and runtime
- **Syntax**: `ENV key=value` or `ENV key value`
- **Inheritance**: Available to all subsequent instructions and running containers

#### 🔌 EXPOSE - Document Ports
```dockerfile
EXPOSE 8080
EXPOSE 3000 8000
EXPOSE 80/tcp 53/udp
```
- **Purpose**: Documents which ports the application uses
- **Note**: Does NOT actually publish ports (use `docker run -p` for that)
- **Best Practice**: Always document the ports your app uses

#### 👤 USER - Set User Context
```dockerfile
# Create and switch to non-root user
RUN useradd -m -s /bin/bash appuser
USER appuser

# Or use numeric UID
USER 1000:1000
```
- **Purpose**: Sets the user for subsequent instructions and container runtime
- **Security**: Avoid running as root in production
- **Default**: Root user (UID 0) if not specified

#### 🚀 CMD vs ENTRYPOINT - Container Startup

**CMD - Default Command (can be overridden)**
```dockerfile
# Exec form (recommended)
CMD ["python", "app.py"]
CMD ["npm", "start"]

# Shell form
CMD python app.py
```

**ENTRYPOINT - Fixed Command (cannot be overridden)**
```dockerfile
# Always runs this command
ENTRYPOINT ["python", "app.py"]

# Combined with CMD for default arguments
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8080"]
```

**Key Differences:**
- `CMD`: Can be overridden by `docker run` arguments
- `ENTRYPOINT`: Always executes, `docker run` args become parameters
- **Best Practice**: Use CMD for most cases, ENTRYPOINT for fixed executables

### Advanced Instructions

#### 📦 ARG - Build Arguments
```dockerfile
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

ARG BUILD_DATE
ARG VERSION=1.0.0
LABEL build_date=${BUILD_DATE}
LABEL version=${VERSION}
```
- **Purpose**: Variables available only during build (not runtime)
- **Usage**: `docker build --build-arg PYTHON_VERSION=3.9 .`

#### 🏷️ LABEL - Metadata
```dockerfile
LABEL maintainer="your.email@example.com"
LABEL version="1.0.0"
LABEL description="My awesome application"
```
- **Purpose**: Adds metadata to images
- **Usage**: Documentation, automation, image management

#### 💾 VOLUME - Persistent Storage
```dockerfile
VOLUME ["/app/data"]
VOLUME /var/log /var/db
```
- **Purpose**: Creates mount points for persistent data
- **Note**: Data in volumes persists even when containers are removed

### Real-World Example

Here's a complete Dockerfile with explanations:

```dockerfile
# Use specific Python version for reproducibility
FROM python:3.11-slim

# Set metadata
LABEL maintainer="developer@company.com"
LABEL version="1.0.0"

# Install system dependencies in one layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv for faster package management
RUN pip install uv

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN uv venv && \
    uv pip install -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -s /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Document the port
EXPOSE 8080

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_ENV=production

# Health check (optional)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Default command
CMD ["python", "app.py"]
```

### 🎯 Dockerfile Best Practices Summary

1. **Order matters**: Put frequently changing instructions last
2. **Minimize layers**: Combine RUN commands with `&&`
3. **Use specific tags**: Avoid `latest` for reproducibility
4. **Security first**: Don't run as root, scan for vulnerabilities
5. **Cache optimization**: Copy requirements before source code
6. **Clean up**: Remove package caches and temporary files

## Docker Compose (Multiple Services)

For applications with multiple services (e.g., web app + database):

### docker-compose.yml
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
```

### Commands
```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs
```

## Best Practices

### 1. Use Specific Tags
```dockerfile
# Good
FROM python:3.9-slim

# Avoid
FROM python:latest
```

### 2. Minimize Layers
```dockerfile
# Good - single RUN command
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean

# Avoid - multiple RUN commands
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean
```

### 3. Use .dockerignore
Create a `.dockerignore` file to exclude unnecessary files:
```
node_modules
.git
*.log
.env
```

### 4. Don't Run as Root
```dockerfile
# Create non-root user
RUN useradd -m myuser
USER myuser
```

## Common Use Cases

### 1. Development Environment
```bash
# Mount current directory to container
docker run -v $(pwd):/app -it python:3.9 bash
```

### 2. Web Application
```dockerfile
FROM node:16
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

### 3. Database
```bash
# Run PostgreSQL container
docker run -d \
  --name my-postgres \
  -e POSTGRES_PASSWORD=mypassword \
  -p 5432:5432 \
  postgres:13
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Use different port
   docker run -p 8081:8080 my-app
   ```

2. **Permission denied**
   ```bash
   # Add user to docker group (Linux)
   sudo usermod -aG docker $USER
   ```

3. **Container exits immediately**
   ```bash
   # Check logs
   docker logs <container_id>
   ```

4. **Out of disk space**
   ```bash
   # Clean up unused containers/images
   docker system prune
   ```

## Useful Commands for Debugging

```bash
# Execute command in running container
docker exec -it <container_id> bash

# Copy files between host and container
docker cp file.txt <container_id>:/app/

# View container resource usage
docker stats

# Inspect container details
docker inspect <container_id>
```

## Next Steps

1. **Learn Docker Compose** for multi-container applications
2. **Explore Docker Hub** for pre-built images
3. **Study container orchestration** with Kubernetes
4. **Implement CI/CD** with Docker in your projects
5. **Learn about security** best practices for containers

## Resources

- [Official Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/) - Repository of container images
- [Play with Docker](https://labs.play-with-docker.com/) - Online Docker playground

---

Remember: Docker containers are ephemeral - data is lost when containers are removed. Use volumes for persistent data storage!

