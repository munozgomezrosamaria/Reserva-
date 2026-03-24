#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
email = 'admin@lagunadelabolsa.com'
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password='adminpassword123', first_name='Administrador')
    print('Superusuario creado automáticamente.')
"
