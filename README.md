# cybersec-proj-backend

This is the backend for the CyberSec project, built using FastAPI, PostgreSQL, and Redis.

## Requirements

- **Docker** (ensures all dependencies are installed within a container)

## Setup & Running the Project

1. Clone the repository

2. Create a .env file in the project root with the necessary environment variable following the formate in env.example

3. Build and Run the Docker Container:
  
  ```python
  docker build -t cybersec-backend-image .
  docker run -d --name cybersec-backend-container --env-file .env -p 8000:8000 cybersec-backend-image

  ```
API Documentation
Once the server is running, visit:

 http://localhost:8000/docs
