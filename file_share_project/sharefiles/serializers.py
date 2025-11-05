from rest_framework import serializers
from .models import SharedFile
"""this class handles conversion between SharedFile model and JSON data for API requests and responses"""
class SharedFileSerializer(serializers.ModelSerializer):
    """meta defines serializer settings to the SharedFile model and shows which fields to read-only."""
    class Meta:
        model=SharedFile
        fields=['id','token','file','is_public','created_at','expires_at']
        read_only_fields=['id','token','created_at']