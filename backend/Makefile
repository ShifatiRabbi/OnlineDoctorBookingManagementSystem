.PHONY: test lint coverage clean

test:
	pytest --cov=. --cov-report=html --cov-report=xml -v

test-verbose:
	pytest -v --tb=short

test-specific:
	pytest $(TEST_PATH) -v

lint:
	flake8 .
	black --check .
	isort --check-only .

format:
	black .
	isort .

coverage:
	pytest --cov=. --cov-report=html
	open htmlcov/index.html

migrations:
	python manage.py makemigrations
	python manage.py migrate

test-docker:
	docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf .coverage htmlcov coverage.xml

ci: lint test