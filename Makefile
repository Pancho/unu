DEV=--file docker-compose.yml

dev-start:
	docker-compose $(DEV) up

dev-build:
	docker-compose $(DEV) build --no-cache

dev-down:
	docker-compose $(DEV) down

dev-web-bash:
	docker-compose $(DEV) exec web bash

dev-web-sql:
	docker-compose $(DEV) exec web python manage.py dbshell

dev-web-django:
	docker-compose $(DEV) exec web python manage.py shell

dev-web-migrate:
	docker-compose $(DEV) exec web python manage.py makemigrations && docker-compose $(DEV) exec web python manage.py migrate
