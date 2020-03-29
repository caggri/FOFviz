from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, blank=True)
    instution = models.CharField(max_length=20, blank=True)
# Create your models here.

    def __str__(self):
        return f"Profile: {self.user}"

def create_user_profile(instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    
post_save.connect(receiver=create_user_profile, sender=User)