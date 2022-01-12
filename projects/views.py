from django.shortcuts import render
from .models import Project, ProjectPermission
# Create your views here.


def index(request):
    projects = Project.objects.all()
    context = {'projects':projects}
    return render(request, 'projects/projects.html', context)


def project(request,pk):
    project = Project.objects.get(id=pk)
    permissions = ProjectPermission.objects.filter(project__name__icontains=project.name)
    context = {'project':project, 'permissions': permissions}
    return render(request,'projects/single-project.html',context)