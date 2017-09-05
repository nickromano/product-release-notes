from __future__ import absolute_import, unicode_literals

import re
from datetime import datetime

import requests

ITUNES_ID_REGEX = re.compile(r'id(?P<itunes_id>[0-9]+)')


def extract_itunes_app_id_from_url(url):
    """
    Example https://itunes.apple.com/us/app/echo-responder-plan-communicate-respond/id916505667
    """
    output = ITUNES_ID_REGEX.search(url)
    if output:
        return output.groupdict()['itunes_id']


class UnableToFindItunesIDException(Exception):
    pass


def current_version_from_itunes(itunes_url):
    itunes_app_id = extract_itunes_app_id_from_url(itunes_url)

    response = requests.get('https://itunes.apple.com/lookup', {'id': itunes_app_id})
    data = response.json()
    if data['resultCount'] != 1:
        raise UnableToFindItunesIDException

    result = data['results'][0]
    release_date = result['currentVersionReleaseDate']
    release_date = datetime.strptime(release_date, '%Y-%m-%dT%H:%M:%SZ')
    return {
        'release_date': release_date,
        'release_notes': result.get('releaseNotes', ''),
        'version': result['version']
    }
