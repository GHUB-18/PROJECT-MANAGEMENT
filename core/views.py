# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db.models import Q

from projects.models import Project
from tasks.models import Task

User = get_user_model()


def index(request):
    if request.user.is_authenticated:
        if not getattr(request.user, 'is_onboarded', True):
            return redirect('onboarding')
        return redirect('dashboard') 
    
    return render(request, 'account/signup.html')


@login_required
def dashboard(request):
    user = request.user

    if not getattr(user, 'is_onboarded', True):
        return redirect('onboarding')

    user_projects = Project.objects.filter(members=user)
    tasks = Task.objects.filter(assigned_to=user).select_related('project')

    if not user_projects.exists():
        messages.info(request, "You are not part of any project yet. Create or join one.")

    # FIXED: Extracting date boundary safely to match Task's DateField type
    current_date = timezone.now().date()
    upcoming_window = current_date + timedelta(days=7)

    context = {
        'projects': user_projects.distinct(),
        
        # REMOVED: Redundant 'sidebar_tasks' context key to let your global context processor handle it.

        'active_projects_count': user_projects.filter(status='active').distinct().count(),
        
        # FIXED: Replaced datetime boundaries with precise date objects
        'tasks_due_soon': tasks.filter(
            due_date__isnull=False,
            due_date__gte=current_date,
            due_date__lte=upcoming_window,
            status__in=['todo', 'in_progress'] # Adjusted choices matching tasks app rules
        ).count(),

        'completed_tasks': tasks.filter(status='done').count(),

        'recent_projects': user_projects.distinct().order_by('-created_at')[:4],
        'assigned_tasks': tasks.exclude(status='done').order_by('due_date')[:5],
    }

    return render(request, 'core/dashboard.html', context)


@login_required
def admin_panel(request):
    if not request.user.is_superuser:
        messages.error(request, "Admin access required.")
        return redirect('dashboard')

    total_users_count = User.objects.count()
    project_queryset = Project.objects.all()

    recent_users = User.objects.order_by('-date_joined')[:25]
    recent_projects = project_queryset.select_related('owner').order_by('-created_at')[:25]

    return render(request, 'core/admin_panel.html', {
        'users': recent_users,
        'projects': recent_projects,
        'total_users': total_users_count,
        'total_projects': project_queryset.count(),
        'active_projects': project_queryset.filter(status='active').count(),
    })


@login_required
def project_list(request):
    if not getattr(request.user, 'is_onboarded', True): 
        return redirect('onboarding')
        
    projects = Project.objects.filter(members=request.user).select_related('owner').order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})


@login_required
def task_list(request):
    if not getattr(request.user, 'is_onboarded', True): 
        return redirect('onboarding')
        
    tasks = Task.objects.filter(assigned_to=request.user).select_related('project').order_by('due_date')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})