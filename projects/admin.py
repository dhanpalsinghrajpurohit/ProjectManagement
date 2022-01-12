from django.contrib import admin
from .models import Project, Permission, ProjectPermission, Task
# Register your models here.
admin.site.register(Project)
admin.site.register(Permission)
admin.site.register(ProjectPermission)
admin.site.register(Task)

