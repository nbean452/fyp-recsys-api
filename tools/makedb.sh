rm -rf base/migrations/ && pipenv run python manage.py makemigrations base && pipenv run python manage.py migrate && pipenv run loaddata && pipenv run python manage.py createsuperuser --noinput
