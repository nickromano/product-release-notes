from __future__ import absolute_import, unicode_literals

from django.shortcuts import render
from django.conf import settings

from .models import ReleaseNote


def release_notes_list(request):
    release_notes = ReleaseNote.objects.published()

    return render(request, 'release_notes/list.html', {
        'release_notes': release_notes,
        'product_name': getattr(settings, 'RELEASE_NOTES_PRODUCT_NAME', ''),
        'page_description': getattr(settings, 'RELEASE_NOTES_PAGE_DESCRIPTION', ''),
        'embed': bool(request.GET.get('embed'))
    })
