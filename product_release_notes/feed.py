from __future__ import absolute_import, unicode_literals

from datetime import datetime, time

from django.conf import settings
from django.contrib.syndication.views import Feed

from .models import ReleaseNote

try:
    from django.urls import reverse
except ImportError:
    # Django 1.8
    from django.core.urlresolvers import reverse


class ReleaseNotesFeed(Feed):
    title = '{} Release Notes'.format(getattr(settings, 'RELEASE_NOTES_PRODUCT_NAME', '')).strip()
    description = getattr(settings, 'RELEASE_NOTES_PAGE_DESCRIPTION', '')

    def link(self):  # noqa
        return reverse('release-notes')

    def items(self):  # noqa
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

    def item_guid(self, item):  # noqa
        return str(item.id)

    def item_pubdate(self, item):  # noqa
        return datetime.combine(item.release_date, time())
