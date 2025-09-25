#!/usr/bin/env bash
set -o errexit

# install dependencies
pip install -r requirements.txt

# Temporarily ensure migrations use the direct Neon URL if provided
if [ -n "$NEON_DIRECT_URL" ]; then
  export DATABASE_URL="$NEON_DIRECT_URL"
fi

# apply migrations
python manage.py migrate --no-input
# collect static files
python manage.py collectstatic --no-input


# create superuser if it doesn't exist
echo "
from django.contrib.auth import get_user_model;
User = get_user_model();
username = 'Victor'
email = 'admin@example.com'
password = 'password'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
" | python manage.py shell
