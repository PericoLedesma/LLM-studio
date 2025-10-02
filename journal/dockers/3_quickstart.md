# Creating Your First Dockerfile

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
    # Build the image in the dockerfile directory
    docker build -t my-app .

    # Run the container
    docker run my-app
```

## Basic Docker Commands

| Group         | Command                                         | Description                                   |
|---------------|-------------------------------------------------|-----------------------------------------------|
| Images        | `docker pull ubuntu`                            | Pull an image from Docker Hub                 |
| Images        | `docker images`                                 | List downloaded images                        |
| Build         | `docker build -t my-app .`                      | Build an image from a Dockerfile              |
| Running       | `docker run ubuntu echo "Hello Docker!"`        | Run a container and execute a command         |
| Running       | `docker run -it my-image sh`                    | Run container interactively                   |
| Running       | `docker run -d nginx`                           | Run container in background (detached)        |
| Running       | `docker run -p 8000:8000 <image_name>`          | Run container and map port 5000 to host       |
| Containers    | `docker ps`                                     | List running containers                       |
| Containers    | `docker ps -a`                                  | List all containers (including stopped ones)  |
| Debugging     | `docker stop <container_id>`                    | Stop a running container                      |
| Debugging     | `docker rm <container_id>`                      | Remove a container                            |
| Debugging     | `docker rmi <image_name>`                       | Remove an image                               |

## Troubleshooting
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

