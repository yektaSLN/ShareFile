from rest_framework import serializers
from .models import SharedFile

"""Handles conversion between SharedFile model and JSON data for API requests and responses"""
class SharedFileSerializer(serializers.ModelSerializer):
    """Meta defines serializer settings for SharedFile model and which fields to be read-only."""
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SharedFile
        fields = ['id', 'token', 'file', 'is_public', 'created_at', 'expires_at', 'user']
        read_only_fields = ['id', 'token', 'created_at', 'user']
