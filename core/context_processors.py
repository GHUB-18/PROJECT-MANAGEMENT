# core/context_processors.py
from django.utils import timezone
from tasks.models import Task
from projects.models import Project

def assigned_tasks_processor(request):
    if request.user.is_authenticated:
        # Fetch tasks assigned to the user that are not completed, ordered by due date
        sidebar_tasks = Task.objects.filter(
            assigned_to=request.user
        ).exclude(
            status='done'
        ).select_related('project').order_by('due_date')[:5] # Limits to top 5 upcoming tasks
        
        return {'sidebar_tasks': sidebar_tasks}
    
    return {'sidebar_tasks': []}

def sidebar_projects(request):
    if request.user.is_authenticated:
        # Fetching all projects the logged-in user participates in
        user_projects = Project.objects.filter(assigned_to=request.user) # Or your specific lookup
        return {'user_projects': user_projects}
    return {'user_projects': []}