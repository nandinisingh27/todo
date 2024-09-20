
from django.urls import path
from . import views



urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('todos/', views.list_todos, name='list_todos'),
    path('todos/create/', views.create_todo, name='create_todo'),
    path('todos/delete/', views.delete_todo, name='delete_todo'),
    path('todos/update/',views.update_todo, name = 'update_todo'),
    path('todos/update_status/',views.update_todo_status, name = 'update_todo_status'),

]


