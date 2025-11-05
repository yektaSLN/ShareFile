from django.urls import path
from . import views
#url patterns for html file
urlpatterns = [
    path('', views.upload_page, name='upload_page'),
]
