from django.core.management.base import BaseCommand
from django.utils import timezone
import os
from sharefiles.models import SharedFile

class Command(BaseCommand):
    """delete expired shared files from the database"""
    help = 'Delete expired files from the system'

    """find and remove expired files"""
    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_files = SharedFile.objects.filter(expires_at__lte=now)
        count = expired_files.count()
        for shared_file in expired_files:
            file_path = shared_file.file.path
            if os.path.exists(file_path):
                os.remove(file_path)
            shared_file.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} expired files.'))
