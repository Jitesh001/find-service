.PHONY: makemigrations migrate run app

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

run:
	python manage.py runserver

app:
	@if [ -z "$(name)" ]; then \
		echo "Error: Please provide an app name using 'make app name=<appname>'"; \
	else \
		python manage.py startapp $(name); \
	fi

superuser:
	python manage.py createsuperuser

sh:
	python manage.py shell