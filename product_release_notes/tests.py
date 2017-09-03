from __future__ import absolute_import, unicode_literals

from datetime import date, datetime

import mock
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase

from .itunes import current_version_from_itunes
from .models import Client, ClientIcons, ReleaseNote
from .templatetags.release_notes import release_notes_feed, MissingRequestTemplateContext


class MockITunesResponse():
    def json(self):
        return {
            "resultCount": 1,
            "results": [
                {
                    "version": "0.0.1",
                    "currentVersionReleaseDate": "2017-07-25T18:54:48Z",
                    "releaseNotes": "New: Added new feature\nFixed: Crash when using feature"
                }
            ]
        }


class ITunesFetchTestCase(TestCase):

    @mock.patch('product_release_notes.itunes.requests.get', return_value=MockITunesResponse())
    def test_itunes_version_api(self, *_):
        itunes_url = 'https://itunes.apple.com/us/app/my-app-name/id3249827349'
        information = current_version_from_itunes(itunes_url)
        self.assertEquals(information, {
            'release_date': datetime(2017, 7, 25, 18, 54, 48),
            'release_notes': 'New: Added new feature\nFixed: Crash when using feature',
            'version': '0.0.1'
        })


class RSSFeedTestCase(TestCase):

    def test_rss_feed_contains_items(self, *_):
        test_client = Client.objects.create(name='iOS', icon=ClientIcons.APPLE)
        test_release_note = ReleaseNote.objects.create(
            client=test_client, release_date=datetime(2017, 9, 1), version='1.0', notes='Initial release'
        )

        response = self.client.get(reverse('release-notes-feed'))
        self.assertFalse('Initial release' in str(response.content))

        test_release_note.is_published = True
        test_release_note.save()

        response = self.client.get(reverse('release-notes-feed'))
        self.assertTrue('Initial release' in str(response.content))

    def test_rss_feed_contains_items_without_versions(self, *_):
        test_client = Client.objects.create(name='iOS', icon=ClientIcons.APPLE)
        ReleaseNote.objects.create(
            client=test_client, release_date=date(2017, 9, 1), notes='Initial release',
            is_published=True
        )

        response = self.client.get(reverse('release-notes-feed'))
        self.assertTrue('Initial release' in str(response.content))


class CheckAppStoreTestCase(TestCase):

    @mock.patch('product_release_notes.management.commands.check_app_stores.mail_admins')
    @mock.patch('product_release_notes.management.commands.check_app_stores.current_version_from_itunes')
    def test_check_app_store_pulls_new_versions(self, mock_current_version, mock_mail_admins, *_):
        mock_current_version.return_value = {
            'version': '1.0',
            'release_notes': 'Initial release',
            'release_date': datetime(2017, 9, 1, 18, 54, 48)
        }

        test_client = Client.objects.create(name='iOS', icon=ClientIcons.APPLE, itunes_url='http://apple.com')

        call_command('check_app_stores')

        mock_mail_admins.assert_called_with(
            'iOS release notes added for version 1.0',
            'Release Notes:\nInitial release\n\nPublish the notes here: //admin/product_release_notes/releasenote/1/\n'
        )

        test_release_note = ReleaseNote.objects.all()[0]
        self.assertEqual(test_release_note.is_published, False)
        self.assertEqual(test_release_note.notes, 'Initial release')
        self.assertEqual(test_release_note.release_date, date(2017, 9, 1))
        self.assertEqual(test_release_note.version, '1.0')
        self.assertEqual(test_release_note.client, test_client)


TEMPLATES_MISSING_CONTEXT_PROCESSOR = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': []
        }
    },
]


class ReleaseNotesPageTestCase(TestCase):

    def test_release_notes_page_only_shows_published(self, *_):
        test_client = Client.objects.create(name='iOS', icon=ClientIcons.APPLE)
        test_release_note = ReleaseNote.objects.create(
            client=test_client, release_date=datetime(2017, 9, 1), version='1.0', notes='Initial release'
        )

        response = self.client.get(reverse('release-notes'))
        self.assertFalse('Initial release' in str(response.content))

        test_release_note.is_published = True
        test_release_note.save()

        response = self.client.get(reverse('release-notes'))
        self.assertTrue('Initial release' in str(response.content))

    def test_release_notes_requires_request_context(self, *_):
        with self.settings(TEMPLATES=TEMPLATES_MISSING_CONTEXT_PROCESSOR):
            with self.assertRaises(MissingRequestTemplateContext):
                self.client.get(reverse('release-notes'))


class MockRequest(object):
    scheme = 'http'

    def get_host(self):
        return 'localhost'


class ReleaseNotesTemplateTagsTestCase(TestCase):

    def test_rss_feed_template_tag_returns_path(self, *_):
        context = {
            'request': MockRequest()
        }
        self.assertEqual(
            release_notes_feed(context),
            '<link rel="alternate" type="application/rss+xml" title="Release Notes RSS Feed" href="http://localhost/feed/">'
        )
