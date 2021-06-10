from django.urls import re_path

from .views import release_notes_list
from .feed import ReleaseNotesFeed

urlpatterns = [
    re_path(r"^$", release_notes_list, name="release-notes"),
    re_path(r"^feed/$", ReleaseNotesFeed(), name="release-notes-feed"),
]
