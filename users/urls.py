from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logoutUser, name='logout'),
    path('updateUser/', views.updateUser, name='update'),
    path('deleteUser/<str:pk>/', views.deleteUser, name='delete'),
    path('account/', views.account, name='account'),
    path('users/', views.users, name='users'),
    path('profile/', views.userProfile, name='profile'),
]
