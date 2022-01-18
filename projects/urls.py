from django.urls import path
from . import views
urlpatterns = [
    path('', views.index,name='home'),
    path('project/<str:pk>/', views.project,name='project'),
    path('project-create/', views.projectCreate,name='project-create'),
    path('project-delete/<str:pk>/', views.projectDelete, name='project-delete'),
    path('project-update/<str:pk>/', views.projectUpdate, name='project-update'),
    path('task-create/<str:pk>/', views.createTask, name='task-create'),
    path('task-update/<str:pk>/<str:type>/', views.updateTask, name='task-update'),
    path('task-delete/<str:pk>/', views.deleteTask, name='task-delete'),
    path('project-share/<str:pk>/', views.projectShare, name='project-share'),
]
