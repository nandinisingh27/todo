
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods
import json
from .models import TodoItem


@require_http_methods(["POST"])
def register(request):
    data = json.loads(request.body)
    first_name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'User already exists!!'},status=400)
    User.objects.create_user(username=username, password=password,first_name = first_name)
    return JsonResponse({'message': 'User created'}, status=201)

@require_http_methods(["POST"])
def login_user(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Logged in'}, status=200)
    return JsonResponse({'error': 'Invalid credentials'}, status=401)


@require_http_methods(["POST"])
def logout_user(request):
    logout(request)
    return JsonResponse({'message': 'Logged out'}, status=200)




@require_http_methods(["POST"])
def create_todo(request):
    data = json.loads(request.body)
    
    title = data.get('title')
    username = data.get('username')
    
    todo = TodoItem(title=title, username = username)
   
    todo.save()
    return JsonResponse({'id': todo.id, 'title': todo.title, 'completed': todo.completed}, status=201)


@require_http_methods(["GET"])
def list_todos(request):
    username =request.GET.get('username')

    todos = TodoItem.objects.filter(username = username )
    todos  =todos.filter(is_deleted = 0)
    
    todos_list = [{'id': todo.id,'username':todo.username ,'title': todo.title, 'completed': todo.completed} for todo in todos ]
    return JsonResponse({'todo':todos_list}, status=200)



@require_http_methods(["PUT"])
def delete_todo(request):
    data = json.loads(request.body)
    id_ = data.get('id')
    task = TodoItem.objects.get(id = id_)
    task.is_deleted = 1
    task.save()
    return JsonResponse({'message': 'Task deleted'}, status=200)


@require_http_methods(["PUT"])
def update_todo(request):
    data = json.loads(request.body)
    id = data.get('id')
    title = data.get('title')
    is_completed = data.get('completed')
    task = TodoItem.objects.get(id = id)
    task.title = title
    task.completed = is_completed
    task.save()
    return JsonResponse({'message': 'Updated successfully'},status =200)

