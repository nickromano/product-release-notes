from __future__ import absolute_import

from django.conf.urls import url

from .views import release_notes_list
from .feed import ReleaseNotesFeed

urlpatterns = [
    url(r'^$', release_notes_list, name='release-notes'),
    url(r'^feed/$', ReleaseNotesFeed(), name='release-notes-feed'),
]
