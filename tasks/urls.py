from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [
    path('project/<int:project_id>/task/create/', views.create_task, name='create_task'),
    path('task/<int:task_id>/toggle/', views.toggle_task_status, name='toggle_task'),
    path('project/<int:project_id>/tasks/', views.task_list, name='task_list'),

]