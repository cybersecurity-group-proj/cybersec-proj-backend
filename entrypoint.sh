#!/bin/bash


set -e

echo "Starting Redis..."
service redis-server start

echo "Starting PostgreSQL..."
service postgresql start

echo "Creating PostgreSQL database and user..."
su - postgres -c "psql -c \"CREATE DATABASE ${DB_NAME};\""
su - postgres -c "psql -c \"CREATE USER ${DB_USERNAME} WITH ENCRYPTED PASSWORD '${DB_PASSWORD}';\""
su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USERNAME};\""

echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
