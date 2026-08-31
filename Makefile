# Velocity Nexus Development & Production Operations

.PHONY: all install build run test clean docker-build docker-up lint format

all: install build run

install:
	pip install -r requirements.txt
	npm install

build:
	npm run build

run:
	python main.py

test:
	pytest tests/ -v --cov=backend --cov=game_servers

lint:
	flake8 backend game_servers tests
	eslint client/core

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov dist build
