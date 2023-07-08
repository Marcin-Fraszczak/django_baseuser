#!/bin/bash

python manage.py migrate
python manage.py create_groups
gunicorn '_config.wsgi'