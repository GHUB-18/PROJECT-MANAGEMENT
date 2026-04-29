from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Using UserAdmin gives you the specialized layout for passwords and permissions
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # This determines what you see in the "User List" view
    list_display = ('username', 'email', 'is_staff', 'is_active')
    
    # This adds the custom fields (like bio or profile_picture) to the edit page
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Profile Info', {'fields': ('bio', 'profile_picture')}),
    )

