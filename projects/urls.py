from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index,name='home'),
    path('project/<str:pk>/', views.project,name='project'),
    path('project-create/', views.projectCreate,name='project-create'),
    path('project-delete/<str:pk>/', views.projectDelete, name='project-delete'),
    path('project-update/<str:pk>/', views.projectUpdate, name='project-update'),
    path('task-create/<str:pk>/', views.createTask, name='task-create'),
]
