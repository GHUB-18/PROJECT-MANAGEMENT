from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from projects.models import Project
from tasks.models import Task
from .forms import TaskForm


# ➕ Create Task
@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # 🔒 Access control: only project members
    if not project.members.filter(pk=request.user.pk).exists():
        messages.error(request, "You do not have permission to add tasks.")
        return redirect('dashboard')

    # 👑 Optional: restrict to owner only
    if project.owner != request.user:
        messages.error(request, "Only the project owner can create tasks.")
        return redirect('project_detail', project_id=project.id)

    form = TaskForm(request.POST or None, project=project)

    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)
        task.project = project
        task.save()

        messages.success(request, "Task created successfully!")
        return redirect('project_detail', project_id=project.id)

    return render(request, "tasks/task_form.html", {
        "form": form,
        "project": project
    })


# ✅ Mark Task as Complete
@login_required
def toggle_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project = task.project

    # 🔒 Access control: must be project member
    if not project.members.filter(pk=request.user.pk).exists():
        messages.error(request, "You do not have access to this task.")
        return redirect('dashboard')

    # 🔒 Only assigned user OR project owner can complete
    if task.assigned_to != request.user and project.owner != request.user:
        messages.error(request, "You cannot complete this task.")
        return redirect('project_detail', project_id=project.id)

    # Prevent re-completion
    if task.status == "done":
        messages.info(request, "Task already completed.")
        return redirect('project_detail', project_id=project.id)

    if request.method == "POST":
        task.status = "done"
        task.completed_at = timezone.now()  # ✅ important
        task.save()

        messages.success(request, "Task marked as completed!")
        return redirect('project_detail', project_id=project.id)

    return render(request, "tasks/confirm_complete.html", {
        "task": task
    })