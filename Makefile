.PHONY: up down build logs migrate seed test lint clean

# Start all services
up:
	docker-compose up -d

# Stop all services
down:
	docker-compose down

# Build all images
build:
	docker-compose build

# Tail logs
logs:
	docker-compose logs -f

# Run Alembic migrations
migrate:
	docker-compose exec backend alembic upgrade head

# Create a new migration
migrate-new:
	docker-compose exec backend alembic revision --autogenerate -m "$(name)"

# Run seed script
seed:
	docker-compose exec backend python -m app.db.seed

# Run tests
test:
	docker-compose exec backend pytest

# Run linter
lint:
	docker-compose exec backend ruff check .
	docker-compose exec backend ruff format --check .

# Clean up volumes
clean:
	docker-compose down -v

# Install backend dependencies
install-backend:
	cd backend && pip install -r requirements.txt

# Install frontend dependencies
install-frontend:
	cd frontend && npm install

# Generate requirements.txt
freeze:
	docker-compose exec backend pip freeze > backend/requirements.txt
