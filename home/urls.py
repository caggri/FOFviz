from django.urls import path
from . import views
from home.dash_apps.finished_apps import sankeydiagram

urlpatterns = [
    path('', views.home, name='home')
]