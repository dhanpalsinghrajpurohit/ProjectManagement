from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ProjectSerializer, TaskSerializer, PermissionSerializer,  ProjectPermissionSerializer, \
    UserSerializer, RegisterSerializer
from projects.models import Project,Task, Permission, ProjectPermission
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from django.contrib.auth import login,authenticate, logout
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

@api_view(['GET'])
def get_users(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


# @api_view(['POST'])
# def signup(request):
#     user = UserSerializer(data=request.data)
#     if user.is_valid():
#         user.save()
#         return Response({"status":"success","message":"created successfully"},status.HTTP_201_CREATED)
#     else:
#         return Response({"status":"failed","message":"error occurred"},status.HTTP_400_BAD_REQUEST)
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


@api_view(['POST'])
def signin(request):
    username = request.data["username"]
    password = request.data["password"]
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid()
    print(serializer)
    user = serializer.data['username']
    login(request, user)
    return Response({
        "user": user,
        "token": AuthToken.objects.create(user)[1]
    })
    # print(username,password)
    # user = User.objects.get(username=username)
    # print(user)
    # if user is not None:
    #     print("work1")
    #     user = authenticate(request, username=username,password=password)
    #     print("work1")
    #     print(user)
    #     if user is not None:
    #         print("work1")
    #         login(request,user)
    #         return Response({"status": "success", "message": "login successfully"}, status.HTTP_201_CREATED)
    # else:
    #     return Response({"status":"failed","message":"username and password are not exit"},status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])      #<pk : project id>
def get_project(request, pk):
    projects = Project.objects.filter(id=pk)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def post_project(request):
    projectserializer = ProjectSerializer(data=request.data)
    if projectserializer.is_valid():
        projectserializer.save()
        return Response({"status": "success", "data": projectserializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "data": projectserializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])       #<pk : project id>
def delete_project(request, pk):
    project = Project.objects.get(id=pk)
    if project.author.id == request.data['userid']:
        if project.delete():
            return Response({"status": "success", "message":"data deleted successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "message":"error occurred."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"status": "error", "message": "unauthorized access."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
def put_project(request):
    project = ProjectSerializer(data=request.data)
    if project.author.id == request.data['userid']:
        if project.is_valid():
            project.save()
            return Response({"status": "success", "data": project.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": project.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"status": "error", "message": "unauthorized access."}, status=status.HTTP_401_UNAUTHORIZED)

# task api ##########################################


@api_view(['GET'])      #<pk=project id>
def get_tasks(request, pk):
    tasks = Task.objects.filter(project__id=pk)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])         #<pk=project id>
def post_task(request, pk):
    project = Project.objects.get(id=pk)
    if project.author.id == request.data['userid']:
        tasks = TaskSerializer(data=request.data)
        if tasks.is_valid():
            tasks.save()
            return Response({"status": "success", "data": tasks.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": tasks.errors, "message": "Error"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"status": "error", "message": "unauthorized access"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])       #<pk=task id>
def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    if task.project.author.id == request.data['userid']:
        if task.delete():
            return Response({"status": "success", "message": "data deleted successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "message": "error occurred."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"status": "error", "message": "unauthorized access."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])      #<pk=project id>
def put_task(request, pk):
    project = Project.objects.get(id=pk)
    if project.author.id == request.data['userid']:
        task = Task.objects.get(id=request.data["id"])
        task = TaskSerializer(data=request.data, instance=task)
        if task.is_valid():
            task.save()
            return Response({"status": "success", "data": task.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": task.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"status": "error", "message": "unauthorized access"}, status=status.HTTP_400_BAD_REQUEST)


# Permission API #############################################

@api_view(['GET'])
def get_permissions(request):
    permissions = Permission.objects.all()
    serializer = PermissionSerializer(permissions, many=True)
    return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_permission(request, pk):
    permission = Permission.objects.filter(id=pk)
    serializer = PermissionSerializer(permission, many=True)
    return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def post_permission(request):
    permission = PermissionSerializer(data=request.data)
    if permission.is_valid():
        permission.save()
        return Response({"status": "success", "data": permission.data}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "data": permission.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_permission(request, pk):
    permission = Permission.objects.get(id=pk)
    if permission.delete():
        return Response({"status": "success", "message": "data deleted successfully."}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "message": "error occurred."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def put_permission(request,pk):
    permission = Permission.objects.get(id=pk)
    serializer = PermissionSerializer(data=request.data,instance=permission)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Project Permission ####################################################

@api_view(['GET'])
def get_projectpermissions(request):
    permissions = ProjectPermission.objects.all()
    serializer = ProjectPermissionSerializer(permissions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_projectpermission(request, pk):
    permissions = ProjectPermission.objects.filter(project__id=pk)
    serializer = ProjectPermissionSerializer(permissions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def post_projectpermission(request):
    permission = ProjectPermissionSerializer(data=request.data)
    if permission.is_valid():
        permission.save()
        return Response({"status": "success", "data": permission.data}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "data": permission.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_projectpermission(request, pk):
    permission = ProjectPermission.objects.filter(project_id=pk)
    if permission.delete():
        return Response({"status": "success", "message": "data deleted successfully."}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "message": "error occurred."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def put_projectpermission(request, pk):
    if request.data['id']:
        permission = ProjectPermission.objects.get(id=request.data['id'])
        permission = ProjectPermissionSerializer(data=request.data,instance=permission)
        if permission.is_valid():
            permission.save()
            return Response({"status": "success", "data": permission.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": permission.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"status": "error", "message": "send correct data"}, status=status.HTTP_400_BAD_REQUEST)