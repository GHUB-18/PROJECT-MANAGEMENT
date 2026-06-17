from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Developer Profiles'
    fk_name = 'user'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'is_staff', 'is_active')
    
    # FIXED: Replaced 'bio' with fields that actually exist on the custom User model
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Profile Info', {'fields': ('profile_picture', 'job_title')}),
    )