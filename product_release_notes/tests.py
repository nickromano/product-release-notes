from __future__ import absolute_import, unicode_literals

from datetime import datetime
import mock

from django.test import TestCase

from .itunes import current_version_from_itunes


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
