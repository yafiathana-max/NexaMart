import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
django.setup()

from django.contrib.auth.models import User

username = "adminuser09"
email = "adminuser09@gmail.com"
password = "Admin@12345"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username,
        email,
        password
    )
    print("Superuser created")
else:
    print("Superuser already exists")