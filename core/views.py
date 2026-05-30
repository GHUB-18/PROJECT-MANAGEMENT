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


# 🌐 Landing / Gateway Route
def index(request):
    if request.user.is_authenticated:
        if not getattr(request.user, 'is_onboarded', True):
            return redirect('onboarding')
        return redirect('dashboard') 
    
    return render(request, 'account/signup.html')


# 📊 Main Application Dashboard View
@login_required
def dashboard(request):
    user = request.user

    # 🔐 SAFETY CHECK: Kick users back to onboarding if they try to bypass it
    if not getattr(user, 'is_onboarded', True):
        return redirect('onboarding')

    # Core user-scoped querysets (Lazy evaluation)
    user_projects = Project.objects.filter(members=user)
    tasks = Task.objects.filter(assigned_to=user).select_related('project')

    # Send a warning message if the user is unassigned across workspaces
    if not user_projects.exists():
        messages.info(request, "You are not part of any project yet. Create or join one.")

    # Calculate deadline window thresholds safely
    now = timezone.now()
    upcoming_window = now + timedelta(days=7)

    context = {
        # Distinct list used purely for rendering the loops
        'projects': user_projects.distinct(),
        
        # Sidebar Tasks Stream
        'sidebar_tasks': tasks.filter(status__in=['pending', 'in_progress']).order_by('due_date')[:10],

        # Key High-Level Performance Counter Aggregates (Optimized without distinct overhead where possible)
        'active_projects_count': user_projects.filter(status='active').distinct().count(),
        
        'tasks_due_soon': tasks.filter(
            due_date__isnull=False,
            due_date__gte=now,
            due_date__lte=upcoming_window,
            status__in=['pending', 'in_progress']
        ).count(),

        'completed_tasks': tasks.filter(status='done').count(),

        # Dashboard Main Content Feeds
        'recent_projects': user_projects.distinct().order_by('-created_at')[:4],
        'assigned_tasks': tasks.exclude(status='done').order_by('due_date')[:5],
    }

    return render(request, 'core/dashboard.html', context)


# 🛠️ System Administration Panel Control Hub
@login_required
def admin_panel(request):
    if not request.user.is_superuser:
        messages.error(request, "Admin access required.")
        return redirect('dashboard')

    # OPTIMIZATION: Use specialized counts instead of putting full tables in memory
    total_users_count = User.objects.count()
    project_queryset = Project.objects.all()

    # Limit list views using slicing or pagination to prevent memory exhaustion
    recent_users = User.objects.order_by('-date_joined')[:25]
    recent_projects = project_queryset.select_related('owner').order_by('-created_at')[:25]

    return render(request, 'core/admin_panel.html', {
        'users': recent_users,
        'projects': recent_projects,
        'total_users': total_users_count,
        'total_projects': project_queryset.count(),
        'active_projects': project_queryset.filter(status='active').count(),
    })


# 📋 Global Project Track Index View 
@login_required
def project_list(request):
    if not getattr(request.user, 'is_onboarded', True): 
        return redirect('onboarding')
        
    projects = Project.objects.filter(members=request.user).select_related('owner').order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})


# 📝 Task Master List View
@login_required
def task_list(request):
    if not getattr(request.user, 'is_onboarded', True): 
        return redirect('onboarding')
        
    tasks = Task.objects.filter(assigned_to=request.user).select_related('project').order_by('due_date')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})