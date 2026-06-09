from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Prefetch
import uuid

from projects.models import Project
from tasks.models import Task
from .forms import ProjectForm


# 🔑 Helper: Generate unique invite token
def generate_unique_token():
    while True:
        token = str(uuid.uuid4())
        if not Project.objects.filter(invite_token=token).exists():
            return token

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related(
            Prefetch('tasks', queryset=Task.objects.order_by('due_date'))
        ),
        id=project_id
    )

    if not project.members.filter(pk=request.user.pk).exists():
        messages.error(request, "You do not have access to this project.")
        return redirect('projects:project_list') # Adjusted fallback

    tasks = project.tasks.all()
    is_owner = (project.owner == request.user)

    context = {
        'project': project,
        'pending_tasks': tasks.exclude(status='done'),
        'completed_tasks': tasks.filter(status='done'),
        'is_owner': is_owner,
    }
    
    if is_owner:
        return render(request, 'projects/project_detail_admin.html', context)
    return render(request, 'projects/project_detail.html', context)


@login_required
def join_project(request, token):
    project = get_object_or_404(Project, invite_token=token)

    if project.members.filter(pk=request.user.pk).exists():
        messages.info(request, "You are already a member of this project.")
    else:
        project.members.add(request.user)
        # FIXED: project.name -> project.title
        messages.success(request, f"Welcome to the team! You successfully joined {project.title}.")

    return redirect('projects:project_detail', project_id=project.id)


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.invite_token = generate_unique_token()
        project.save()

        # Safely handling M2M roster insertion here
        project.members.add(request.user)

        messages.success(request, "Project workspace deployed successfully!")
        return redirect('projects:project_list') 

    return render(request, 'projects/create_project.html', {'form': form})


@login_required
def leave_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.user == project.owner:
        messages.error(request, "Workspace owners cannot abandon their project. Delete it instead.")
    else:
        project.members.remove(request.user)
        # FIXED: project.name -> project.title
        messages.success(request, f"You successfully left {project.title}.")
        
    return redirect('projects:project_list')


@login_required
def project_list(request):
    projects = Project.objects.filter(members=request.user).order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})


@login_required
def admin_panel(request):
    if not request.user.is_superuser:
        messages.error(request, "Access restricted to system administrators.")
        return redirect('projects:project_list')
    return render(request, "projects/admin_panel.html")


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.owner:
        messages.error(request, "You do not have management permissions to alter this workspace.")
        return redirect('projects:project_list')

    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project details updated successfully!")
        return redirect('projects:project_detail', project_id=project.id)

    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})


@login_required
def project_settings(request, project_id):
    return redirect('projects:project_detail', project_id=project_id)


@login_required
def archive_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    # FIXED: project.name -> project.title
    messages.success(request, f'"{project.title}" has been archived.')
    return redirect('projects:project_list')