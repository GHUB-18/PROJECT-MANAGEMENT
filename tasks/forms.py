from django import forms
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'priority']

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)  # 👈 get project
        super().__init__(*args, **kwargs)

        # Title
        self.fields['title'].widget.attrs.update({
            'placeholder': 'e.g., Design Landing Page',
            'class': 'form-input'
        })

        # Description
        self.fields['description'].widget = forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'What are the requirements for this task?',
            'class': 'form-input'
        })

        # Assigned to (ONLY project members)
        if project:
            self.fields['assigned_to'].queryset = project.members.all()
        else:
            self.fields['assigned_to'].queryset = User.objects.none()

        self.fields['assigned_to'].empty_label = "Select a team member"
        self.fields['assigned_to'].required = False

        # Due date
        self.fields['due_date'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-input'
        })

        # Priority
        self.fields['priority'].widget.attrs.update({
            'class': 'form-input'
        })