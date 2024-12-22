from django.contrib import admin

# Register your models here.
from .models import Client, Project, Task, Employee, WorkLog

admin.site.register(Client)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Employee)
admin.site.register(WorkLog)