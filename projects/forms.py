from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'color_theme']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded-lg',
                'placeholder': 'e.g. Website Redesign'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded-lg',
                'rows': 4
            }),
            'color_theme': forms.Select(attrs={
                'class': 'w-full p-2 border rounded-lg'
            }),
        }