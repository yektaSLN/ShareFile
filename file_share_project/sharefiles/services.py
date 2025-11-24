from django.utils import timezone
from .models import SharedFile

class SharedFileService:
    @staticmethod
    def create_shared_file(user, file_obj, is_public=False, days=3):
        """create a new shared file and set its expiry"""
        shared_file = SharedFile.objects.create(
            user=user,
            file=file_obj,
            is_public=is_public
        )
        shared_file.expires_at = timezone.now() + timezone.timedelta(days=days)
        shared_file.save()
        return shared_file

    @staticmethod
    def get_shared_file_by_token(token):
        """get a file by token and check for expiration """
        try:
            file_obj = SharedFile.objects.get(token=token)
        except SharedFile.DoesNotExist:
            return None, "not_found"

        if file_obj.expires_at and timezone.now() >= file_obj.expires_at:
            return file_obj, "expired"
        return file_obj, None

    @staticmethod
    def delete_expired_files():
        """delete all expired files from db"""
        now = timezone.now()
        expired_files = SharedFile.objects.filter(expires_at__lte=now)
        count = expired_files.count()

        for file_obj in expired_files:
            if file_obj.file and file_obj.file.storage.exists(file_obj.file.path):
                file_obj.file.delete(save=False)
            file_obj.delete()

        return count

    @staticmethod
    def delete_expired_files_by_token(token):
        """delete a specific file by token """
        try:
            file_obj = SharedFile.objects.get(token=token)
        except SharedFile.DoesNotExist:
            return 0

        if file_obj.file and file_obj.file.storage.exists(file_obj.file.path):
            file_obj.file.delete(save=False)
        file_obj.delete()
        return 1
