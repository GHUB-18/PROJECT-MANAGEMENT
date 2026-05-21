from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

from projects.models import Project
from tasks.models import Task

User = get_user_model()


# 🌐 Landing / Gateway Route
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard') 
    else:
        return render(request, 'account/signup.html')


# 📊 Main Application Dashboard View
@login_required
def dashboard(request):
    user = request.user

    # OPTIMIZATION: Prefetch and filter projects the user belongs to down to a distinct list
    projects = Project.objects.filter(members=user).distinct()

    # Tasks assigned to user (optimized lookup)
    tasks = Task.objects.filter(assigned_to=user).select_related('project')

    if not projects.exists():
        messages.info(request, "You are not part of any project yet. Create or join one.")

    # Calculate deadline window thresholds
    upcoming_window = timezone.now() + timedelta(days=7)

    context = {
        # Global collections needed by both base layouts and sidebar inclusion tracks
        'projects': projects,
        'sidebar_tasks': tasks.filter(status__in=['pending', 'in_progress']).order_by('due_date')[:10],

        # Key High-Level Performance Counter Aggregates
        'active_projects_count': projects.filter(status='active').count(),
        
        'tasks_due_soon': tasks.filter(
            due_date__lte=upcoming_window,
            status__in=['pending', 'in_progress']
        ).count(),

        'completed_tasks': tasks.filter(status='done').count(),

        # Dashboard Main Content Feeds (Optimized for rendering cards with related model data)
        'recent_projects': projects.order_by('-created_at')[:4],
        'assigned_tasks': tasks.exclude(status='done').order_by('due_date')[:5],
    }

    return render(request, 'core/dashboard.html', context)


# 🛠️ System Administration Panel Control Hub
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


# 📋 Global Project Track Index View 
@login_required
def project_list(request):
    projects = Project.objects.filter(members=request.user).select_related('owner').order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})


# 📝 Task Master List View
@login_required
def task_list(request):
    tasks = Task.objects.filter(assigned_to=request.user).select_related('project').order_by('due_date')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})