from django.core.files.storage import default_storage
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from .serializers import SharedFileSerializer
from django.http import HttpResponseRedirect, JsonResponse
from .models import SharedFile

class SharedFileViewSet(viewsets.ModelViewSet):
    queryset = SharedFile.objects.all()
    serializer_class = SharedFileSerializer  # ✅ fixed here

    def create(self, request, *args, **kwargs):
        """handle uploading a file.users send the file,
        optionally set public status and expiry days."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shared_file = serializer.save()

        days = request.data.get('days', 3)
        try:
            shared_file.set_expiry_days(int(days))
        except ValueError:
            shared_file.set_expiry_date(3)
        return Response(self.get_serializer(shared_file).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def serve_by_token(request, token):
    """access file by its token"""
    file_obj = get_object_or_404(SharedFile, token=token)
    if file_obj.is_expired():
        return Response({'detail': 'This link has expired.'}, status=status.HTTP_410_GONE)
    if not file_obj.is_public:
        return Response({'detail': 'This file is private.'}, status=403)
    return HttpResponseRedirect(file_obj.file.url)

"""uploading the html template"""
def upload_page(request):
    return render(request, 'upload.html')
