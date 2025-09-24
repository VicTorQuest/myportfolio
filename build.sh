#!/usr/bin/env bash
set -o errexit

# install dependencies
pip install -r requirements.txt

# collect static files
python manage.py collectstatic --no-input

# apply migrations
python manage.py migrate

# create superuser if it doesn't exist
echo "
from django.contrib.auth import get_user_model;
User = get_user_model();
username = 'admin'
email = 'admin@example.com'
password = 'password'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
" | python manage.py shell
