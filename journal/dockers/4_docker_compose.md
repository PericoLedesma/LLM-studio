# Docker Compose for Dummies 🚢

## What is Docker Compose?

Docker Compose is like having a **conductor for an orchestra** - it coordinates multiple Docker containers to work together as a single application. Instead of running containers one by one with complex commands, you define everything in a simple YAML file.

Think of it this way:
- **Docker** = Individual musicians (containers)
- **Docker Compose** = The conductor who makes them play in harmony

## Why Use Docker Compose?

### Before Docker Compose (The Hard Way 😰)
```bash
  # Run a database
  docker run -d --name mydb -e POSTGRES_PASSWORD=secret postgres:13

  # Run a web app
  docker run -d --name myapp -p 3000:3000 --link mydb:db myapp:latest

  # Run a cache
  docker run -d --name redis -p 6379:6379 redis:alpine

  # Clean up (if you remember all the names!)
  docker stop mydb myapp redis
  docker rm mydb myapp redis
```

### With Docker Compose (The Easy Way 😎)
```bash
  # Start everything
  docker-compose up

  # Stop everything
  docker-compose down
```

## Basic Docker Compose File Structure

Create a file called `docker-compose.yml`:

```yaml
  version: '3.8'

  services:
    web:
      build: .
      ports:
        - "3000:3000"
      depends_on:
        - db
        - redis

    db:
      image: postgres:13
      environment:
        POSTGRES_PASSWORD: secret
      volumes:
        - postgres_data:/var/lib/postgresql/data

    redis:
      image: redis:alpine
      ports:
        - "6379:6379"

  volumes:
    postgres_data:
```

## Key Concepts Explained

### 1. Services
Each service is a container. In the example above:
- `web` - Your application
- `db` - PostgreSQL database
- `redis` - Redis cache

### 2. Images vs Build
```yaml
  # Use a pre-built image
  db:
    image: postgres:13

  # Build from Dockerfile
  web:
    build: .
```

### 3. Ports
```yaml
  ports:
    - "3000:3000"  # host:container
    - "8080:80"    # map host port 8080 to container port 80
```

### 4. Environment Variables
```yaml
  environment:
    - NODE_ENV=production
    - DATABASE_URL=postgres://user:pass@db:5432/mydb
```

### 5. Volumes
```yaml
  volumes:
    - ./data:/app/data        # Bind mount
    - postgres_data:/var/lib/postgresql/data  # Named volume
```

### 6. Dependencies
```yaml
  depends_on:
    - db      # Start db before web
    - redis   # Start redis before web
```

## Common Commands

### Basic Operations
| Command                                 | Description                                      |
|------------------------------------------|--------------------------------------------------|
| `docker-compose up`                      | Start all services                               |
| `docker-compose up -d`                   | Start all services in background (detached)      |
| `docker-compose down`                    | Stop all services                                |
| `docker-compose logs`                    | View logs for all services                       |
| `docker-compose logs web`                | View logs for specific service (`web`)           |
| `docker-compose up --build`              | Rebuild images and start all services            |
| `docker-compose up web db`               | Start only specific services (`web`, `db`)       |
| `docker-compose exec web bash`           | Execute a bash shell in the running `web` service|
| `docker-compose exec db psql -U postgres`| Open a psql shell in the running `db` service    |

## Real-World Example: Full-Stack App

Here's a complete example for a Node.js + PostgreSQL + Redis app:

```yaml
version: '3.8'

services:
  # Frontend (React)
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:5000
    depends_on:
      - backend

  # Backend (Node.js API)
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://postgres:secret@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app
      - /app/node_modules

  # Database
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  # Cache
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  # Nginx (Reverse Proxy)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend
      - backend

volumes:
  postgres_data:
```

## Pro Tips 💡

### 1. Use .env Files
Create a `.env` file:
```bash
  POSTGRES_PASSWORD=mysecretpassword
  NODE_ENV=development
```

Reference in docker-compose.yml:
```yaml
  environment:
    - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    - NODE_ENV=${NODE_ENV}
```

### 2. Override for Different Environments
Create `docker-compose.override.yml` for development:
```yaml
  version: '3.8'
  services:
    web:
      volumes:
        - .:/app  # Live reload
      environment:
        - DEBUG=true
```

### 3. Health Checks
```yaml
  services:
    web:
      image: myapp
      healthcheck:
        test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
        interval: 30s
        timeout: 10s
        retries: 3
```

### 4. Resource Limits
```yaml
  services:
    web:
      image: myapp
      deploy:
        resources:
          limits:
            memory: 512M
            cpus: '0.5'
```

## Troubleshooting Common Issues

### 1. Port Already in Use
```bash
  # Find what's using the port
  lsof -i :3000

  # Kill the process or change the port in docker-compose.yml
```

### 2. Services Not Starting
```bash
  # Check logs
  docker-compose logs service_name

  # Check if containers are running
  docker-compose ps
```

### 3. Database Connection Issues
- Make sure `depends_on` is set correctly
- Use service names as hostnames (e.g., `db:5432`)
- Check environment variables

## Quick Reference Card

| Command | Description |
|---------|-------------|
| `docker-compose up` | Start all services |
| `docker-compose up -d` | Start in background |
| `docker-compose down` | Stop and remove containers |
| `docker-compose down -v` | Stop and remove volumes too |
| `docker-compose logs` | View all logs |
| `docker-compose logs -f` | Follow logs |
| `docker-compose ps` | List running containers |
| `docker-compose exec service bash` | Run command in service |
| `docker-compose build` | Build images |
| `docker-compose pull` | Pull latest images |


