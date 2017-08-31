from __future__ import absolute_import, unicode_literals

from datetime import datetime, time

from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.conf import settings

from .models import ReleaseNote


class ReleaseNotesFeed(Feed):
    title = '{} Release Notes'.format(getattr(settings, 'RELEASE_NOTES_PRODUCT_NAME', '')).strip()
    description = getattr(settings, 'RELEASE_NOTES_PAGE_DESCRIPTION', '')

    @property
    def link(self):
        return reverse('release-notes')

    @property
    def items(self):
        return ReleaseNote.objects.published()[:10]

    def item_title(self, item):
        if item.version:
            return '{} {}'.format(
                item.client.name,
                item.version
            )

        return '{} {}'.format(
            item.client.name,
            item.release_date.strftime('%x')
        )

    def item_description(self, item):
        return item.notes.replace('\n', '<br />')

    def item_link(self, item):
        return reverse('release-notes')

    @property
    def item_guid(self, obj):
        return str(obj.id)

    @property
    def item_pubdate(self, item):
        return datetime.combine(item.release_date, time())
