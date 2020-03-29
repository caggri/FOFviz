from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register')
    # path('password/', views.change_password, name='change_password'),


]
