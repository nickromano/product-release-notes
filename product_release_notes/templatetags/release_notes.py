import re

from django import template
from django.utils.html import format_html

try:
    from django.urls import reverse
except ImportError:
    # Django 1.8
    from django.core.urlresolvers import reverse


register = template.Library()


FEED_HTML = """
<link rel="alternate"
      type="application/rss+xml"
      title="Release Notes RSS Feed"
      href="{scheme}://{host}{feed_url}">
"""


class MissingRequestTemplateContext(Exception):
    ERROR_MESSAGE = (
        "django.template.context_processors.request "
        "to your TEMPLATES context_processors"
    )


@register.simple_tag(takes_context=True)
def release_notes_feed(context):
    scheme = ''
    host = ''

    try:
        request = context['request']
    except KeyError:
        raise MissingRequestTemplateContext(
            MissingRequestTemplateContext.ERROR_MESSAGE
        )

    scheme = request.scheme
    host = request.get_host()

    feed_url = FEED_HTML.format(
        scheme=scheme,
        host=host,
        feed_url=reverse('release-notes-feed')
    )
    # Clean up newlines and extra space
    feed_url = feed_url.replace('\n', '')
    feed_url = re.sub(' +', ' ', feed_url)

    return format_html(feed_url)
