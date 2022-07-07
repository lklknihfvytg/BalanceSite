from django.urls import path
from . import views

app_name = 'General'

urlpatterns = [
    path('', views.homepage_views, name = 'homepage_views'),
]
