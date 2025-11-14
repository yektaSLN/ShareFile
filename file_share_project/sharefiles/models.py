from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from datetime import timedelta

def user_file_path(instance, filename):
    """return upload path for each users file"""
    if instance.user:
        return f'uploads/{instance.user.username}/{instance.token}/{filename}'
    return f'uploads/anonymous/{instance.token}/{filename}'


class SharedFile(models.Model):
    """model for a shared file"""
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="shared_files"
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    file = models.FileField(upload_to=user_file_path, max_length=255)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def set_expiry_days(self, days=3):
        """set expire date 'days' days from now"""
        self.expires_at = timezone.now() + timedelta(days=days)
        self.save()

    def is_expired(self):
        """check if the link is expired"""
        return self.expires_at and timezone.now() >= self.expires_at

    def __str__(self):
        """return string form of the file token"""
        return f"{self.user.username if self.user else 'Anonymous'} - {self.token}"
