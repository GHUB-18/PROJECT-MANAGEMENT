from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Project, Task, ProjectFile, Membership, Activity
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
# 1. Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Grab the email from the POST data manually
            user.email = request.POST.get('email') 
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'projects/register.html', {'form': form})

# 2. Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Find the user associated with this email
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid password.")
        except User.objects.DoesNotExist:
            messages.error(request, "No account found with that email.")
            
    return render(request, 'projects/login.html')

# 3. Dashboard (Home Page)
@login_required # This sends them to login if they aren't authenticated
def dashboard(request):
    # Only show projects where the user is a member or leader
    projects = Project.objects.filter(members=request.user) | Project.objects.filter(leader=request.user)
    return render(request, 'dashboard.html', {'projects': projects.distinct()})

# 4. Project Detail View
@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    # Filter tasks based on completion status
    pending_tasks = project.tasks.filter(is_completed=False).order_by('deadline')
    completed_tasks = project.tasks.filter(is_completed=True).order_by('-completed_at')
    
    context = {
        'project': project,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
    }
    return render(request, 'project_detail.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')