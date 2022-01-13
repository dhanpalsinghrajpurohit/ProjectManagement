from django.shortcuts import render, redirect
from .models import Project, ProjectPermission, Task
from django.contrib.auth.models import User
from users.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm,  TaskForm
from django.forms import forms
# Create your views here.


def index(request):
    projects = Project.objects.all()
    context = {'projects':projects}
    return render(request, 'projects/projects.html', context)


def project(request,pk):
    project = Project.objects.get(id=pk)
    permissions = project.projectpermission_set.filter(user__id=request.user.id)
    permission = []
    for per in permissions:
        permission.append(per.permission.name)
    tasks = Task.objects.filter(project__id__icontains=project.id)
    context = {'project': project, 'permissions': permission, 'tasks': tasks}
    return render(request,'projects/single-project.html',context)


@login_required(login_url='signin')
def projectCreate(request):
    profile = request.user.first_name
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            return redirect('account')
    context = {'form': form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url='signin')
def projectUpdate(request, pk):
    profile = request.user
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            return redirect('account')
    context = {'form': form, 'project': project}
    return render(request, "projects/project_form.html", context)


@login_required(login_url='signin')
def projectDelete(request,pk):
    project = Project.objects.get(id=pk)
    project.delete()
    messages.success(request, "project deleted successfully.")
    return redirect('home')


def tasks(request):
    tasks = Task.objects.get(id=pk)
    pass


def createTask(request, pk):
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project', pk=pk)
    context = {'form': form, 'id': pk}
    return render(request, 'projects/task_form.html',context)


def updateTask(request):
    pass


def deleteTask(request,pk):
    task = Task.objects.get(id=pk)
    task.delete()
    messages.success(request,"Task was deleted successfully.")
    return redirect('home')