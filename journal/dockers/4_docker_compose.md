# Docker Compose for Dummies 🚢

## What is Docker Compose?

Docker Compose is like having a **conductor for an orchestra** - it coordinates multiple Docker containers to work together as a single application. Instead of running containers one by one with complex commands, you define everything in a simple YAML file.

Think of it this way:
- **Docker** = Individual musicians (containers)
- **Docker Compose** = The conductor who makes them play in harmony


### Docker Compose (The Easy Way 😎)
```bash
  # Start everything
  docker-compose up

  # Stop everything
  docker-compose down
```

## Basic Docker Compose File Structure (docker-compose.yml)

```yaml
version: '3.8'

services:
  quickstart-app:
    build:
      context: ./quickstart
      dockerfile: Dockerfile
    container_name: quickstart-container
    ports:
      - "8000:8000"
    environment:
      - FLASK_APP=app.py
      - FLASK_RUN_HOST=0.0.0.0
      - FLASK_RUN_PORT=5000
    volumes:
      - ./quickstart:/app
    restart: unless-stopped
```

## Key Concepts Explained

- **version: '3.8'**  
  Specifies the version of the Docker Compose file format.

- **services:**  
  This section lists all the containers (services) you want to run. In this example, there is one service called `quickstart-app`.

  - **quickstart-app:**  
    The name of the service.

    - **build:**  
      Tells Docker Compose to build the image from a Dockerfile.
      - `context: ./quickstart` — The directory containing the Dockerfile and app code.
      - `dockerfile: Dockerfile` — The Dockerfile to use.

    - **container_name:**  
      Sets a custom name for the running container (`quickstart-container`).

    - **ports:**  
      Maps port 5000 on your host to port 5000 in the container (`"5000:5000"`), so you can access the app at `localhost:5000`.

    - **environment:**  
      Sets environment variables inside the container, configuring Flask to run the app and listen on all interfaces (`0.0.0.0`) and port 5000.

    - **volumes:**  
      Mounts the local `./quickstart` directory into `/app` inside the container. This allows live code changes on your host to be reflected in the container.

    - **restart:**  
      Configures the container to restart automatically unless it is explicitly stopped.


### What is a Service?
A service in docker-compose.yml defines:
What image to use (or how to build one)
How to run the container (ports, environment variables, volumes, etc.)
Configuration for the container's behavior


**How it works:**  
When you run `docker-compose up`, Docker Compose will:
1. Build the image for `quickstart-app` using the specified Dockerfile.
2. Start the container with the given environment variables and port mappings.
3. Mount your code into the container for easy development.
4. Automatically restart the container if it crashes.


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


