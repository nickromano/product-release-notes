import re

from django import template
from django.utils.html import format_html
from django.core.urlresolvers import reverse

register = template.Library()


FEED_HTML = """
<link rel="alternate"
      type="application/rss+xml"
      title="Release Notes RSS Feed"
      href="{scheme}://{host}{feed_url}">
"""


@register.simple_tag(takes_context=True)
def release_notes_feed(context):
    scheme = ''
    host = ''

    request = context.get('request')
    if request:
        scheme = request.scheme
        host = request.META['HTTP_HOST']

    feed_url = FEED_HTML.format(
        scheme=scheme,
        host=host,
        feed_url=reverse('release-notes-feed')
    )
    # Clean up newlines and extra space
    feed_url = feed_url.replace('\n', '')
    feed_url = re.sub(' +', ' ', feed_url)

    return format_html(feed_url)
