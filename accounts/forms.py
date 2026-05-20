# accounts/forms.py

from allauth.socialaccount.forms import SignupForm
from django import forms


class CustomSocialSignupForm(SignupForm):

    first_name = forms.CharField(max_length=30)

    last_name = forms.CharField(max_length=30)

    username = forms.CharField(max_length=150)

    email = forms.EmailField()

    job_title = forms.CharField(max_length=100)

    def save(self, request):

        user = super().save(request)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.job_title = self.cleaned_data['job_title']

        user.save()

        return user