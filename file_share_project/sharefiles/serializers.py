from rest_framework import serializers
from .models import SharedFile

"""Handles conversion between SharedFile model and JSON data for API requests and responses"""
class SharedFileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True, help_text="Owner of the file")
    file = serializers.FileField(help_text="Uploaded file")
    is_public = serializers.BooleanField(help_text="True if the file is public")
    expires_at = serializers.DateTimeField(help_text="Expiry date of the file")


    """Meta defines serializer settings for SharedFile model and which fields to be read-only."""
    class Meta:
        model = SharedFile
        fields = ['id', 'token', 'file', 'is_public', 'created_at', 'expires_at', 'user']
        read_only_fields = ['id', 'token', 'created_at', 'user']