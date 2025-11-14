from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .serializers import SharedFileSerializer
from .models import SharedFile
from .services import SharedFileService

class SharedFileViewSet(viewsets.ModelViewSet):
    queryset = SharedFile.objects.all()
    serializer_class = SharedFileSerializer

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)

    def create(self, request, *args, **kwargs):
        """handle uploading a file with optional public status and expiry days"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user if request.user.is_authenticated else None
        file_obj = request.data.get('file')
        is_public = request.data.get('is_public', False)
        days = request.data.get('days', 3)

        try:
            days = int(days)
        except ValueError:
            days = 3

        shared_file = SharedFileService.create_shared_file(
            user=user,
            file_obj=file_obj,
            is_public=is_public,
            days=days
        )

        return Response(self.get_serializer(shared_file).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='serve')
    def serve_by_token(self, request, pk=None):
        """serve a file by its token"""
        token = pk
        file_obj, error = SharedFileService.get_shared_file_by_token(token)

        if error == "expired":
            return Response({'detail': 'This link has expired.'}, status=status.HTTP_410_GONE)
        if not file_obj.is_public:
            return Response({'detail': 'This file is private.'}, status=status.HTTP_403_FORBIDDEN)


        return Response({
            'id': file_obj.id,
            'token': str(file_obj.token),
            'file_url': file_obj.file.url,
            'is_public': file_obj.is_public,
            'created_at': file_obj.created_at,
            'expires_at': file_obj.expires_at
        })
