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
            Prefetch('task_set', queryset=Task.objects.order_by('due_date'))
        ),
        id=project_id
    )

    # 🔒 Access control
    if not project.members.filter(pk=request.user.pk).exists():
        messages.error(request, "You do not have access to this project.")
        return redirect('dashboard')

    tasks = project.task_set.all()

    context = {
        'project': project,
        'pending_tasks': tasks.exclude(status='done'),
        'completed_tasks': tasks.filter(status='done'),
        'is_owner': project.owner == request.user,
    }

    return render(request, 'core/project_detail.html', context)


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
        messages.success(request, f"You joined {project.title}!")

    return redirect('project_detail', project_id=project.id)


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