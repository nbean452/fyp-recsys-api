trash db.sqlite3 && trash base/migrations/ && pipenv run python manage.py makemigrations base && pipenv run python manage.py migrate && pipenv run loaddata
