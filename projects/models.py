from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.


class Permission(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000,null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


class Project(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(null=True, blank=True, default="images/default.jpg")
    project_color_identity = models.CharField(max_length=200,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


class ProjectPermission(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.permission)


class Task(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=uuid.uuid4)
    description = models.CharField(max_length=200, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, default=uuid.uuid4)

    def __str__(self):
        return str(self.name)