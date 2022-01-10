from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,blank=False)
    email = models.CharField(max_length=200, blank=False)
    password = models.CharField(max_length=200,blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

