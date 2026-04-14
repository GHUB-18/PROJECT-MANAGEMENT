from django.contrib import admin
from .models import Project, Task, ProjectFile, Membership, Activity

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(ProjectFile)
admin.site.register(Membership)
admin.site.register(Activity)


