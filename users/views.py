from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.models import User
# Create your views here.


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
            # login(request, user)
            return redirect('signin')
        else:
            messages.error(request, 'Error has occurred during the registration!')

    context = {'form': form, 'page': page}
    return render(request, 'users/user_signup.html', context)


def signin(request):
    page = 'signin'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        print(request)
        username = request.POST['txt_username']
        password = request.POST['txt_password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exits..')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,"Error has occurred during the registration.. ")
    context = {'page': page}
    return render(request,'users/user_signup.html',context)


def logoutUser(request):
    logout(request)
    messages.info(request, "User has been logged out!")
    return redirect('signin')
