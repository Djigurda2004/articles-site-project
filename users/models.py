from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    followers = models.ManyToManyField(User,symmetrical=False,related_name="following",blank=True)

    def __str__(self):
        return self.user.username