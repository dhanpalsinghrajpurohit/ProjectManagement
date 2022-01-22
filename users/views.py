from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm,ProfileForm
from django.contrib import messages
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.models import User
from .models import Profile
from projects.models import ProjectPermission
# Create your views here.


def users(request):
    user = User.objects.all()
    context = {'users':user}
    return render(request, 'users/users.html', context)


def signup(request):
    page = "signup"
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User account was created successfully..")
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error has occurred during the registration!')
    context = {'form': form, 'page': page}
    return render(request, 'users/user_signup.html', context)


def signin(request):
    page = 'signin'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST['txt_username']
        password = request.POST['txt_password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exits..')
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Please! Enter a valid password ")
    context = {'page': page}
    return render(request,'users/user_signup.html',context)


def updateUser(request):
    page = 'update'
    form = CustomUserCreationForm(instance=request.user)
    if request.method == "POST":
        form = CustomUserCreationForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Details updated successfully..")
            return redirect('home')
    context = {'form': form, 'page': page}
    return render(request, 'users/user_form.html', context)


def account(request):
    user = request.user
    # print(user.author.profile)
    projects = user.project_set.filter(author__id=user.id)
    permissions = ProjectPermission.objects.all()
    context = {'user':user, 'projects':projects}
    return render(request, 'users/account.html', context)


def userProfile(request):
    form = ProfileForm()
    if request.method == "POST":
        print(request.FILES['profile_picture'])
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        form = Profile(username=request.user,profile_picture=request.FILES['profile_picture'])
        # print(form.is_valid())
        # if form.is_valid():
        #     print(form.save())
        form.save()
        return redirect('users')
    context = {'form': form}
    return render(request, 'users/user_image_form.html', context)


def deleteUser(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    messages.success(request, "user deleted successfully.")
    return redirect('home')


def logoutUser(request):
    logout(request)
    messages.info(request, "User has been logged out!")
    return redirect('signin')
