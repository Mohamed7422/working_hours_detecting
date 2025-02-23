from django.contrib import admin
from django.db.models import Count, Sum
from .models import Client, Project, Task, Employee, WorkLog



# Create your custom ClientAdmin
class ClientAdmin(admin.ModelAdmin):
    change_list_template = "admin_templates/client_change_list.html"

    def changelist_view(self, request, extra_context=None):
        # Get the default changelist response
        response = super().changelist_view(request, extra_context)
        # Query all clients and annotate a project count
        qs = self.model.objects.all().annotate(project_count=Count('project'))
        
        # Prepare data for the pie chart
        client_names = [client.client_name for client in qs]
        project_counts = [client.project_count for client in qs]

        # Pass your chart data into the template context
        response.context_data['client_names'] = client_names
        response.context_data['project_counts'] = project_counts

        return response

class WorkLogAdmin(admin.ModelAdmin):
    # Using Django's built-in list_filter for related fields:
    list_filter = ('employee', 'task__project')
    change_list_template = "admin_templates/worklog_change_list.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        # Get filtered queryset from the changelist view (if present)
        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            qs = self.model.objects.all()
        
        # Group the WorkLogs by task and sum hours_logged
        chart_data = (
            qs.values('task__task_name')
              .annotate(total_time=Sum('hours_logged'))
              .order_by('task__task_name')
        )
        tasks = [entry['task__task_name'] for entry in chart_data]
        total_time = [float(entry['total_time']) for entry in chart_data]

        response.context_data['chart_tasks'] = tasks
        response.context_data['chart_total_time'] = total_time
        return response
    
class ProjectAdmin(admin.ModelAdmin):
    change_list_template = "admin_templates/project_change_list.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        qs = self.model.objects.all()
        # Sum the worklog hours for each project via its tasks (some projects may not have worklogs)
        qs = qs.annotate(total_time=Sum('task__worklog__hours_logged'))
        project_names = [project.project_name for project in qs]
        # Use 0 if no worklog hours are present
        total_hours = [float(project.total_time or 0) for project in qs]

        response.context_data['project_names'] = project_names
        response.context_data['total_hours'] = total_hours
        return response

 

   
try:
    admin.site.unregister(Project)
except admin.sites.NotRegistered:
    pass
admin.site.register(Project, ProjectAdmin) 

# Unregister if necessary then register our custom admin
try:
    admin.site.unregister(WorkLog)
except admin.sites.NotRegistered:
    pass
admin.site.register(WorkLog, WorkLogAdmin)      

# If Client was already registered, unregister it first:
try:
    admin.site.unregister(Client)
except admin.sites.NotRegistered:
    pass
admin.site.register(Client, ClientAdmin)





# Register other models
#admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Employee)