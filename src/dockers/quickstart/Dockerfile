# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application file from the current directory
# COPY app.py .

# copy all(Local files or remote URLs)
COPY . .

# copy all (Local files only)
# ADD . .


# install dependencies
# RUN pip install -r requirements.txt
# RUN pip install time

# Set a env variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Port number that needs to be exposed
EXPOSE 5000


# Run the application
CMD ["python", "app.py"]