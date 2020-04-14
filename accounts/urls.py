from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.register, name='register'),
    # path('password/', views.change_password, name='change_password'),
    path('edit/', views.edit_profile, name="edit"),
    path('profile/', views.profile, name="profile"),
    path('password/', views.change_password, name="change_password"),
    path('logout', include('django.contrib.auth.urls'), name='logout')

]
