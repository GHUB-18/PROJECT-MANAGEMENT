from django.urls import path
from . import views
from core import views as core_views
from tasks import views as task_views

urlpatterns = [
    # Main dashboard 
    
    # Project view
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('join/<uuid:token>/', views.join_project, name='join_project'),
    path('create/', views.create_project, name='create_project'),

    path('project/<int:project_id>/task/create/', task_views.create_task, name='create_task'),
    path('task/<int:task_id>/toggle/', task_views.toggle_task_status, name='toggle_task'),

    # path('project/<int:project_id>/task/create/', views.create_task, name='create_task'),
    # path('task/<int:task_id>/toggle/', views.toggle_task_status, name='toggle_task'),
    

]