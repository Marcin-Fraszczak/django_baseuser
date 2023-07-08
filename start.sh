#!/bin/bash

python manage.py migrate
python manage.py create_groups
python manage.py collectstatic
python manage.py createsuperuser --noinput
gunicorn '_config.wsgi'