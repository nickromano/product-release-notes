from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.mail import mail_admins
from django.core.management.base import BaseCommand
from product_release_notes.itunes import current_version_from_itunes
from product_release_notes.models import Client, ReleaseNote


MAIL_MESSAGE = """Release Notes:
{notes}

Publish the notes here: {base_url}/admin/product_release_notes/releasenote/{release_id}/
"""


def send_email_notification(client, current_version, release_note):
    if getattr(settings, 'DISABLE_RELEASE_NOTES_NOTIFICATION', False):
        return

    mail_admins(
        '{} release notes added for version {}'.format(
            client.name, current_version
        ),
        MAIL_MESSAGE.format(
            notes=release_note.notes,
            base_url=getattr(settings, 'BASE_URL', '/'),
            release_id=release_note.id
        )
    )


class Command(BaseCommand):
    help = 'Checks iTunes and Google Play for new versions and creates drafts.'

    def success_message(self, message):
        if hasattr(self.style, 'SUCCESS'):
            self.stdout.write(self.style.SUCCESS(message))
        else:
            # Django 1.8
            self.stdout.write(self.style.MIGRATE_SUCCESS(message))

    def handle(self, *args, **options):
        for client in Client.objects.exclude(itunes_url=''):
            itunes_information = current_version_from_itunes(client.itunes_url)
            current_version = itunes_information['version']

            release_note, created = ReleaseNote.objects.get_or_create(
                client=client, version=current_version,
                defaults={
                    'notes': itunes_information['release_notes'],
                    'release_date': itunes_information['release_date']
                }
            )
            if created:
                self.success_message('Version changed for {} {}'.format(client, current_version))
                send_email_notification(client, current_version, release_note)

        self.success_message('Checked iTunes')
