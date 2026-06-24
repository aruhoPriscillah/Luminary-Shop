#!/usr/bin/env bash
set -e

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_data

# Create site and superuser
python manage.py shell << 'EOF'
from django.contrib.sites.models import Site

# Delete all existing sites and create fresh
Site.objects.all().delete()
Site.objects.create(id=1, domain='luminary-shop.onrender.com', name='luminary-shop.onrender.com')
print('Site created successfully!')
EOF