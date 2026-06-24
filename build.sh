#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_data
python manage.py shell -c "
from django.contrib.sites.models import Site
site, created = Site.objects.get_or_create(id=1)
site.domain = 'luminary-shop.onrender.com'
site.name = 'luminary-shop.onrender.com'
site.save()
print('Site updated!')
"