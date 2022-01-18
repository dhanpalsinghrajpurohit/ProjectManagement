from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_picture = models.ImageField(null=True,blank=True,upload_to="profiles/",default="images/default.jpg")

    def __str__(self):
        return str(self.username)


