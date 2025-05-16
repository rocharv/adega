help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

admin: ## run inside Django env: django-admin [command]
	@poetry run django-admin $(filter-out $@,$(MAKECMDGOALS))


createcachetable: ## run inside Django env: createcachetable
	@poetry run python manage.py createcachetable select2_cache_table

createsuperuser: ## run inside Django env: createsuperuser
	@poetry run python manage.py createsuperuser

docker-down: ## run inside Docker env: docker-compose down
	@docker compose down

docker-prune: ## run inside Docker env: docker-compose prune
	@docker system prune -a --volumes --force

docker-up: ## run inside Docker env: docker-compose up
	@docker compose up -d

makemigrations: ## run inside Django env: makemigrations
	@poetry run python manage.py makemigrations

manage: ## run inside Django env: manage.py [command]
	@poetry run python manage.py $(filter-out $@,$(MAKECMDGOALS))

migrate: ## run inside Django env: migrate
	@poetry run python manage.py migrate

runserver: ## run inside Django env: runserver
	@poetry run python manage.py runserver

shell: ## run inside Django env: shell
	@poetry run python manage.py shell
