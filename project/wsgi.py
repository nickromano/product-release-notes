"""
WSGI config for project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


def setup_whitenoise(app):
    try:
        from whitenoise.django import DjangoWhiteNoise
    except ImportError:
        # Not running in heroku
        return

    return DjangoWhiteNoise(app)  # noqa


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

application = get_wsgi_application()  # noqa
application = setup_whitenoise(application)  # noqa
