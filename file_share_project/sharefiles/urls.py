from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SharedFileViewSet

router = DefaultRouter()
router.register(r'files', SharedFileViewSet, basename='files')

urlpatterns = [
    path('', include(router.urls)),
]
