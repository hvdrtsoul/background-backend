#!/bin/sh

cd /app

echo "Applying migrations"
python manage.py makemigrations
python manage.py migrate --noinput

python manage.py runserver