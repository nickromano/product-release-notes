./manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_USERNAME', '$SUPERUSER_PASSWORD')" | python manage.py shell
