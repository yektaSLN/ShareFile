from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SharedFileViewSet, serve_by_token

#create a router for RESTAPI endpoints
router = DefaultRouter()
router.register(r'files', SharedFileViewSet, basename='files')

#defining URL patterns for the app
urlpatterns = [
    path('', include(router.urls)),  # API endpoints like /api/files/
    path('f/<uuid:token>/', serve_by_token, name='serve-by-token'),
]
