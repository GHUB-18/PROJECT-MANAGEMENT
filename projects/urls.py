# projects/urls.py
from django.urls import path
from . import views
from core import views as core_views
from tasks import views as task_views

app_name = "projects"

urlpatterns = [
    path('create/', views.create_project, name='create_project'),

    path('join/<str:token>/', views.join_project, name='join_project'),
    path('edit/<int:project_id>/', views.edit_project, name='edit_project'),
    path('leave/<int:project_id>/', views.leave_project, name='leave_project'),

    path('admin/', views.admin_panel, name='admin_panel'),

    path('<int:project_id>/', views.project_detail, name='project_detail'),



]