run:
	docker-compose up --build

test:
	hatch run pytest

lint:
	hatch run black src
	hatch run isort src
	hatch run mypy src

stop:
	docker-compose down
