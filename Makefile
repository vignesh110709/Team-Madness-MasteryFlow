.PHONY: dev test seed proof format

dev:
	docker-compose up --build

test:
	echo "Running tests..."

seed:
	echo "Seeding data..."

proof:
	echo "Running proofs..."

format:
	echo "Formatting code..."
