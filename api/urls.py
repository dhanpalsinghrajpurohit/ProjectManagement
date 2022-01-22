from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('users/', views.get_users),
    path('user-signup/',views.RegisterAPI.as_view()),
    path('user-signin/',views.LoginAPI.as_view()),

    path('projects/', views.get_projects),
    path('project/<str:pk>/', views.get_project),   #<pk : project id>
    path('project-post/', views.post_project),
    path('project-delete/<str:pk>/', views.delete_project),     #<pk : project id>
    path('project-put/', views.put_project),

    path('tasks/<str:pk>/', views.get_tasks),       #<pk=project id>
    path('task-post/<str:pk>/', views.post_task),       #<pk=project id>
    path('task-delete/<str:pk>/', views.delete_task),       #<pk=task id>
    path('task-put/<str:pk>/', views.put_task),         #<pk=project id>

    path('projectpermissions/', views.get_projectpermissions),
    path('projectpermission/<str:pk>/', views.get_projectpermission),       #<pk:project_id>
    path('projectpermission-post/', views.post_projectpermission),
    path('projectpermission-delete/<str:pk>/', views.delete_projectpermission),
    path('projectpermission-put/<str:pk>/', views.put_projectpermission),       #<pk:project_id>
    #
    path('permissions/', views.get_permissions),
    path('permission/<str:pk>/', views.get_permission),  #<pk:permission id>
    path('permission-post/', views.post_permission),
    path('permission-delete/<str:pk>/', views.delete_permission), #<pk:permission  id>
    path('permission-put/<str:pk>/', views.put_permission), #<pk:permissio id>

]