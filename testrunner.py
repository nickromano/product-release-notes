import os
import sys

from django.conf import settings

import django


def runtests():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, test_dir)

    settings.configure(
        DEBUG=True,
        SECRET_KEY='123',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3'
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'product_release_notes'
        ],
        ROOT_URLCONF='product_release_notes.urls',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
            },
        ]
    )
    django.setup()

    from django.test.utils import get_runner
    TestRunner = get_runner(settings)  # noqa
    test_runner = TestRunner(verbosity=1, interactive=True)
    if hasattr(django, 'setup'):
        django.setup()
    failures = test_runner.run_tests(['product_release_notes'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()
