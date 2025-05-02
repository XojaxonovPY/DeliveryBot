
extract:
	pybabel extract --input-dirs=. -o locales/messages.pot
init:
	pybabel init -i locales/messages.pot -d locales -D messages -l uz
	pybabel init -i locales/messages.pot -d locales -D messages -l ru
compile:
	pybabel compile -d locales -D messages
update:
	pybabel update -d locales -D messages -i locales/messages.pot
webs:
	uvicorn web.app:app --host localhost --port 8005

mig:
	alembic revision --autogenerate -m "Create a baseline migrations"
upg:
	alembic upgrade head
downgrade:
	alembic downgrade head
alembic_init:
	alembic init migrations
