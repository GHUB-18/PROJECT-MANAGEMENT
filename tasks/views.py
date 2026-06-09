from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from projects.models import Project
from tasks.models import Task
from .forms import TaskForm


@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # Access control: only project members
    if not project.members.filter(pk=request.user.pk).exists():
        messages.error(request, "You do not have permission to add tasks.")
        return redirect('projects:project_list') # FIXED: Namespaced fallbacks

    # Restrict creation to workspace owner
    if project.owner != request.user:
        messages.error(request, "Only the project owner can create tasks.")
        return redirect('projects:project_detail', project_id=project.id) # FIXED namespace

    form = TaskForm(request.POST or None, project=project)

    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)
        task.project = project
        task.save()

        messages.success(request, "Task created successfully!")
        return redirect('projects:project_detail', project_id=project.id) # FIXED namespace

    return render(request, "tasks/task_form.html", {
        "form": form,
        "project": project
    })


@login_required
def toggle_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project = task.project

    if not project.members.filter(pk=request.user.pk).exists():
        messages.error(request, "You do not have access to this task.")
        return redirect('projects:project_list') # FIXED namespace

    if task.assigned_to != request.user and project.owner != request.user:
        messages.error(request, "You cannot complete this task.")
        return redirect('projects:project_detail', project_id=project.id) # FIXED namespace

    if task.status == "done":
        messages.info(request, "Task already completed.")
        return redirect('projects:project_detail', project_id=project.id) # FIXED namespace

    if request.method == "POST":
        task.status = "done"
        task.completed_at = timezone.now() 
        task.save()

        messages.success(request, "Task marked as completed!")
        return redirect('projects:project_detail', project_id=project.id) # FIXED namespace

    return render(request, "tasks/confirm_complete.html", {"task": task})


@login_required
def task_list(request, project_id):
    # Verify user belongs to the project before displaying tasks
    project = get_object_or_404(Project, id=project_id, members=request.user)
    
    # FIXED: Isolated query scope to project_id target
    tasks = Task.objects.filter(
        project=project, 
        assigned_to=request.user
    ).order_by('-created_at')
    
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'project': project
    })