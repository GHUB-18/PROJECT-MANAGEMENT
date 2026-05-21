from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Prefetch
from django.utils import timezone
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


# 🏠 Project Detail View
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
        return redirect('dashboard')

    tasks = project.tasks.all()

    context = {
        'project': project,
        'pending_tasks': tasks.exclude(status='done'),
        'completed_tasks': tasks.filter(status='done'),
        'is_owner': project.owner == request.user,
    }

    return render(request, 'projects/project_detail.html', context)


# 🔗 Join Project (via invite token)
@login_required
def join_project(request, token):
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('dashboard')

    project = get_object_or_404(Project, invite_token=token)

    if project.members.filter(pk=request.user.pk).exists():
        messages.info(request, "You are already a member of this project.")
    else:
        project.members.add(request.user)
        # FIXED: Field attribute changed from .title to match your template attribute (.name)
        messages.success(request, f"You joined {project.name}!")

    # FIXED: Added required 'projects:' namespace prefix to redirect safely
    return redirect('projects:project_detail', project_id=project.id)


# ➕ Create Project
@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.invite_token = generate_unique_token()
        project.save()

        project.members.add(request.user)

        messages.success(request, "Project created successfully!")
        return redirect('dashboard')

    return render(request, 'projects/create_project.html', {'form': form})


# 🚪 Leave Project
@login_required
def leave_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user == project.owner:
        messages.error(request, "Owners cannot leave their own project. Delete it instead.")
    else:
        project.members.remove(request.user)
        # FIXED: Updated field attribute mapping from .title to .name
        messages.success(request, f"You left {project.name}.")
    return redirect('dashboard')


# 📋 Project List Index
# FIXED: Added missing login restriction decorator to block anonymous users from querying database relationships
@login_required
def project_list(request):
    projects = Project.objects.filter(members=request.user).order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})


# 🛠️ Admin Dashboard Panel
@login_required
def admin_panel(request):
    # Optional security layer: verify user is actually an administrator before rendering
    if not request.user.is_superuser:
        messages.error(request, "Access restricted to administrators.")
        return redirect('dashboard')
    return render(request, "projects/admin_panel.html")

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.owner:
        messages.error(request, "You are not allowed to edit this project.")
        return redirect('dashboard')

    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project updated successfully!")
        return redirect('projects:project_detail', project_id=project.id)

    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})