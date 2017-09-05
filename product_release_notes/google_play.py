from __future__ import absolute_import, unicode_literals

from datetime import datetime

import requests
from bs4 import BeautifulSoup


def current_version_from_google(google_play_url):
    response = requests.get(google_play_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    release_notes = soup.find(class_="recent-change").get_text()
    release_date_text = soup.find(itemprop="datePublished").get_text()

    release_date = datetime.strptime(release_date_text, '%B %d, %Y').date()

    return {
        'release_date': release_date,
        'release_notes': release_notes
    }
