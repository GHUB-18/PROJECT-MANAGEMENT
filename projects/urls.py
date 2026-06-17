from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    # Added root list route path
    path('', views.project_list, name='project_list'),
    
    path('create/', views.create_project, name='create_project'),
    path('join/<str:token>/', views.join_project, name='join_project'),
    path('admin/', views.admin_panel, name='admin_panel'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('<int:project_id>/settings/', views.project_settings, name='project_settings'),
    path('<int:project_id>/archive/', views.archive_project, name='archive_project'),
    path('<int:project_id>/leave/', views.leave_project, name='leave_project'),
]