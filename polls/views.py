import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

from django.http import JsonResponse

import json
from .models import TodosItem




def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        if not bool(re.match(r"^[A-Za-z][A-Za-z0-9_]{1,29}$",username)):
            return JsonResponse({'error':'Enter a valid username , Username should contain alphabets and numbers,it should not contain spaces and special characters except underscores'},status =401)
        first_name = data.get('name')

        if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,15}$",first_name)):
            return JsonResponse({'error':'Enter a valid name, it should not contain numbers'},status =401)
        password = data.get('password')
        cpassword = data.get('cpassword')
        if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",password)):
            return JsonResponse({'error':'password must  contain atleast a special character,a uppercase letter, a lowercase letter,a number and minimum should be of 8 character'},status =401)
        if password != cpassword:
            return JsonResponse({'error':'Password and confirm password do not match'},status = 401)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'User already exists!!'},status=400)
        User.objects.create_user(username=username, password=password,first_name = first_name)
        return JsonResponse({'message': 'User created'}, status=201)
    else:
        return JsonResponse({'error':'Invalid method'},status = 405)


def login_user(request):
    if request.method =="POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if username is None:
            return JsonResponse({'error':'Please enter username'})
        if password is None:
            return JsonResponse({'error':'Please enter password'})
        user = authenticate(request , username=username, password=password)
        if user is not None:
            login(request, user)
            username = request.user
            
            return JsonResponse({'id': user.id, 'username': user.username}, status=200)
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    else:
        return JsonResponse({'error':'Invalid method'},status = 405)
    
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({'message':'Logged out!!'},status = 200)
    else:
        return JsonResponse({'error':'Invalid method'},status =405 )





def create_todo(request):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get('title')
        if title is not None:
            if not bool(re.match("^[A-Za-z0-9 _]*[A-Za-z0-9][A-Za-z0-9 _]*$",title)):
                return JsonResponse({'error':'enter a valid task to add'},status=400)
            username = request.user
            print(username)
            todo = TodosItem(title=title, username = username)
            todo.save()
            return JsonResponse({'id': todo.id, 'title': todo.title, 'completed': todo.completed}, status=201)
        else:
            return JsonResponse({'error':'task field cannot be empty'},status = 400)
    else:
        return JsonResponse({'error':'Invalid method'},status =405 )




def list_todos(request):
    if request.method == "GET":
        username = request.user
        print(username)
    if not username.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    todos = TodosItem.objects.filter(username =username)
    todos  =todos.filter(is_deleted = 0)
    
    todos_list = [{'id': todo.id,'username':todo.username ,'title': todo.title, 'completed': todo.completed} for todo in todos ]
    return JsonResponse({'todo':todos_list}, status=200)



def delete_todo(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        id_ = data.get('id')
        task = TodosItem.objects.get(id = id_)
        task.is_deleted = 1
        task.save()
        return JsonResponse({'message': 'Task deleted'}, status=200)
    else:
        return JsonResponse({'error':'Invalid method'},status = 405)



def update_todo(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        id = data.get('id')
        title = data.get('title')
        is_completed = data.get('completed')
        if not is_completed :
            print(is_completed)
            if title is not None:
                    if not bool(re.match("^[A-Za-z0-9 _]*[A-Za-z0-9][A-Za-z0-9 _]*$",title)):
                        return JsonResponse({'error':'enter a valid task to add'},status=400)
                    task = TodosItem.objects.get(id = id)
                    task.title = title
                    task.completed = is_completed
                    task.save()
                    return JsonResponse({'message': 'Updated successfully'},status =200)
            else:
                return JsonResponse({'error':'task field cannot be empty'}, status =400)
        else:
            return JsonResponse({'error':'Task is already completed,cannot edit it'},status =400)
    else:
        return JsonResponse({'error':'Invalid method'},status = 405)


       
    
              

def update_todo_status(request):
    if request.method=="PUT":
        data = json.loads(request.body)
        id = data.get('id')
        is_completed = data.get('completed')
        task = TodosItem.objects.get(id = id)
        task.completed = is_completed
        task.save()
        return JsonResponse({'message': ' Status updated successfully'},status =200)    
    else:
        return JsonResponse({'error':'Invalid method'},status = 405) 

    
            
     