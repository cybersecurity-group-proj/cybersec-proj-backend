#!/bin/bash


set -e


echo "Starting Redis..."
service redis-server start

echo "Starting PostgreSQL..."
service postgresql start

echo "Creating PostgreSQL database and user..."
su - postgres -c "psql -c \"CREATE DATABASE ${DB_NAME};\""
su - postgres -c "psql -c \"CREATE USER ${DB_USERNAME} WITH ENCRYPTED PASSWORD '${DB_PASSWORD}';\""
su - postgres -c "psql -c \"ALTER USER ${DB_USERNAME} WITH SUPERUSER;\""


echo "Running Alembic migrations..."
alembic upgrade head

# Run the database initialization script
echo "Running database initialization..."
python app/db/initialize_db.py


echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
