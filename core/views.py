from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from projects.models import Project
from tasks.models import Task

User = get_user_model()

def index(request):
    if request.user.is_authenticated:
        # If logged in, send them to the dashboard or main app
        return redirect('dashboard') 
    else:
        # If guest, show them the signup/login page
        return render(request, 'account/signup.html')

@login_required
def dashboard(request):
    user = request.user

    # Projects user belongs to
    projects = Project.objects.filter(members=user).distinct()

    # Tasks assigned to user
    tasks = Task.objects.filter(assigned_to=user)

    if not projects.exists():
        messages.info(request, "You are not part of any project yet. Create or join one.")

    context = {
        'projects': projects,

        'active_projects_count': projects.filter(status='active').count(),

        'tasks_due_soon': tasks.filter(
            due_date__lte=timezone.now() + timedelta(days=7),
            status__in=['pending', 'in_progress']
        ).count(),

        'completed_tasks': tasks.filter(status='done').count(),

        'recent_projects': projects.order_by('-created_at')[:4],

        'assigned_tasks': tasks.exclude(status='done')[:5],
    }

    return render(request, 'core/dashboard.html', context)


@login_required
def admin_panel(request):
    if not request.user.is_superuser:
        messages.error(request, "Admin access required.")
        return redirect('dashboard')

    users = User.objects.all()
    projects = Project.objects.all()

    return render(request, 'core/admin_panel.html', {
        'users': users,
        'projects': projects,
        'total_users': users.count(),
        'total_projects': projects.count(),
        'active_projects': projects.filter(status='active').count(),
    })

@login_required
def project_list(request):
    # Get all projects where the user is a member
    projects = Project.objects.filter(members=request.user).order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def task_list(request):
    # Get all tasks assigned to the user
    tasks = Task.objects.filter(assigned_to=request.user).order_by('due_date')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})