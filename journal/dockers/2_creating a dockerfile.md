## 📋 Dockerfile Instructions Explained

A Dockerfile is a script containing a series of instructions that Docker uses to build an image. Each instruction creates a new layer in the image.

### 🎯 Dockerfile Best Practices Summary
1. **Order matters**: Put frequently changing instructions last
2. **Minimize layers**: Combine RUN commands with `&&`
3. **Use specific tags**: Avoid `latest` for reproducibility
4. **Security first**: Dont run as root, scan for vulnerabilities
5. **Cache optimization**: Copy requirements before source code
6. **Clean up**: Remove package caches and temporary files


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
- **Creates**: The directory if it doesnt exist
- **Affects**: All following RUN, CMD, COPY, ADD instructions
- **Example**: WORKDIR /app means all operations happen in /app

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
- **Best Practice**: Use COPY unless you specifically need ADDs features

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

Heres a complete Dockerfile with explanations:

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
