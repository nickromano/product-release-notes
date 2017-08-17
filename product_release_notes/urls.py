from __future__ import absolute_import

from django.conf.urls import url

from .views import release_notes

urlpatterns = [
    url(r'$', release_notes, name='release-notes'),
]
