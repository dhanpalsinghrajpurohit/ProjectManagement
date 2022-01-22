from django.shortcuts import render, redirect
from .models import Project, ProjectPermission, Task
from django.contrib.auth.models import User
from users.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from .forms import ProjectForm, TaskForm, PermissionForm
from django.forms import forms


# Create your views here.


@login_required(login_url='signin')
def index(request):
    # permission = ProjectPermission.objects.filter(user__id=request.user.id)
    # temp = Project.projectpermission_set.get(id)
    # print(temp)
    print(request.user.has_perm('Project.view_projects'))
    projects = Project.objects.filter()
    context = {'projects': projects}
    return render(request, 'projects/projects.html', context)


@login_required(login_url='signin')
def project(request, pk):
    try:
        project = Project.objects.get(id=pk)
        permission = []
        try:
            permissions = project.projectpermission_set.get(user__id=request.user.id)
            permissions = permissions.permission.all()
            for per in permissions:
                if per == "DELETE" or per == "UPDATE" or per == "VIEW":
                    permission.append(per)
                else:
                    permission.append(per.name)
        except:
            pass
    except Project.DoesNotExist:
        return redirect('home')
    tasks = Task.objects.filter(project__id__icontains=project.id)
    context = {'project': project, 'permissions': permission, 'tasks': tasks}
    return render(request, 'projects/single-project.html', context)


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
    # project = profile.project_set.get(id=pk)
    try:
        project = Project.objects.get(id=pk)
        form = ProjectForm(instance=project)
        if request.method == "POST":
            form = ProjectForm(request.POST, request.FILES, instance=project)
            if form.is_valid():
                form.save()
                return redirect('project',pk=project.id)

    except Project.DoesNotExist:
        return redirect('home')
    context = {'form': form, 'project': project}
    return render(request, "projects/project_form.html", context)


@login_required(login_url='signin')
def projectDelete(request, pk):
    project = Project.objects.get(id=pk)
    project.delete()
    messages.success(request, "project deleted successfully.")
    return redirect('home')


def projectShare(request, pk):
    data = Project.objects.get(id=pk)
    form = PermissionForm(initial={'project': data})
    if request.method == "POST":
        form = PermissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project', pk=form.instance.project.id)
    context = {'form': form}
    return render(request, 'projects/shareform.html', context)


# def tasks(request,pk):
#     tasks = Task.objects.filter(project__id=pk)
#     context = {'tasks':tasks}
#     return render(request, '')
#     pass


def createTask(request, pk):
    data = Project.objects.get(id=pk)
    form = TaskForm(initial={'project': data})
    if request.method == "POST":
        if request.user == data.author:
            form = TaskForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('project', pk=form.instance.project.id)
    context = {'form': form}
    return render(request, 'projects/task_form.html', context)


def updateTask(request, pk, type):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project', pk=form.instance.project.id)
    context = {'form': form}
    return render(request, 'projects/task_form.html', context)


def deleteTask(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    messages.success(request, "Task was deleted successfully.")
    return redirect('project', pk=task.project.id)
