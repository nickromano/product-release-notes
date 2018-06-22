from __future__ import absolute_import, unicode_literals

from datetime import date, datetime

import mock
from django.core.management import call_command
from django.test import TestCase

from .google_play import current_version_from_google
from .itunes import current_version_from_itunes
from .models import Client, ClientIcons, ReleaseNote
from .templatetags.release_notes import (
    MissingRequestTemplateContext, release_notes_feed
)

try:
    from django.urls import reverse
except ImportError:
    # Django 1.8
    from django.core.urlresolvers import reverse


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
    def test_check_itunes_pulls_new_versions(self, mock_current_version, mock_mail_admins, *_):
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

    @mock.patch('product_release_notes.management.commands.check_app_stores.mail_admins')
    @mock.patch('product_release_notes.management.commands.check_app_stores.current_version_from_google')
    def test_check_google_play_pulls_new_versions(self, mock_current_version, mock_mail_admins, *_):
        mock_current_version.return_value = {
            'release_notes': 'Initial release',
            'release_date': datetime(2017, 9, 1, 18, 54, 48)
        }

        test_client = Client.objects.create(name='Android', icon=ClientIcons.ANDROID, google_play_url='http://play.google.com')

        call_command('check_app_stores')

        mock_mail_admins.assert_called_with(
            'Android release notes added for version September 01, 2017',
            'Release Notes:\nInitial release\n\nPublish the notes here: //admin/product_release_notes/releasenote/1/\n'
        )

        test_release_note = ReleaseNote.objects.all()[0]
        self.assertEqual(test_release_note.is_published, False)
        self.assertEqual(test_release_note.notes, 'Initial release')
        self.assertEqual(test_release_note.release_date, date(2017, 9, 1))
        self.assertEqual(test_release_note.version, '')
        self.assertEqual(test_release_note.client, test_client)

    @mock.patch('product_release_notes.management.commands.check_app_stores.mail_admins')
    @mock.patch('product_release_notes.management.commands.check_app_stores.current_version_from_google')
    def test_check_google_play_auto_publish(self, mock_current_version, mock_mail_admins, *_):
        mock_current_version.return_value = {
            'release_notes': 'Initial release',
            'release_date': datetime(2017, 9, 1, 18, 54, 48)
        }

        Client.objects.create(name='Android', icon=ClientIcons.ANDROID, google_play_url='http://play.google.com')

        with self.settings(RELEASE_NOTES_AUTO_PUBLISH=True):
            call_command('check_app_stores')

        test_release_note = ReleaseNote.objects.all()[0]
        self.assertEqual(test_release_note.is_published, True)

    @mock.patch('product_release_notes.management.commands.check_app_stores.mail_admins')
    @mock.patch('product_release_notes.management.commands.check_app_stores.current_version_from_itunes')
    def test_check_itunes_auto_publish(self, mock_current_version, mock_mail_admins, *_):
        mock_current_version.return_value = {
            'version': '1.0',
            'release_notes': 'Initial release',
            'release_date': datetime(2017, 9, 1, 18, 54, 48)
        }

        Client.objects.create(name='iOS', icon=ClientIcons.APPLE, itunes_url='http://apple.com')

        with self.settings(RELEASE_NOTES_AUTO_PUBLISH=True):
            call_command('check_app_stores')

        test_release_note = ReleaseNote.objects.all()[0]
        self.assertEqual(test_release_note.is_published, True)


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


html_doc = """
<div class="details-wrapper">
    <div class="details-section whatsnew">
        <div class="details-section-contents show-more-container">
            <h1 class="heading"> What's New </h1>
            <div class="recent-change">New version release notes</div>
        </div>
        <div class="details-section-divider"></div>
    </div>
</div>
<div class="details-wrapper apps-secondary-color">
    <div class="details-section metadata">
        <div class="details-section-heading">
            <h1 class="heading"> Additional information </h1>
        </div>
        <div class="details-section-contents">
            <div class="meta-info">
                <div class="title">Updated</div>
                <div class="content" itemprop="datePublished">December 14, 2016</div>
            </div>
            <div class="meta-info">
                <div class="title">Current Version</div>
                <div class="content" itemprop="softwareVersion"> Varies with device </div>
            </div>
            <div class="meta-info">
                <div class="title">Requires Android</div>
                <div class="content" itemprop="operatingSystems"> Varies with device </div>
            </div>
        </div>
        <div class="details-section-divider"></div>
    </div>
</div>
"""


class MockGooglePlayRequest():
    text = html_doc

    def raise_for_status(self):
        pass


class GooglePlayFetchTestCase(TestCase):

    @mock.patch('product_release_notes.google_play.requests.get', return_value=MockGooglePlayRequest())
    def test_google_play_version_api(self, *_):
        current_version = current_version_from_google('')
        self.assertEqual(current_version['release_date'], date(2016, 12, 14))
        self.assertEqual(current_version['release_notes'], 'New version release notes')
