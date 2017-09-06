from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from .models import Client, ReleaseNote


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'itunes_url', 'google_play_url',
        'created', 'modified',
    )


@admin.register(ReleaseNote)
class ReleaseNoteAdmin(admin.ModelAdmin):
    list_display = (
        'release_date', 'version', 'notes', 'is_published', 'client',
        'created', 'modified',
    )
    list_filter = ('client__name', 'is_published',)
    list_select_related = ('client',)
    date_hierarchy = 'release_date'
