from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [
    path("create/<int:project_id>/", views.create_task, name="create_task"),
    path("<int:task_id>/toggle/", views.toggle_task_status, name="toggle_task_status"),
    path("list/<int:project_id>/", views.task_list, name="task_list"),


]