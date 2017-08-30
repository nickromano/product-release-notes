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
    request = context['request']

    return format_html(FEED_HTML.format(
        scheme=request.scheme,
        host=request.META['HTTP_HOST'],
        feed_url=reverse('release-notes-feed')
    ))
