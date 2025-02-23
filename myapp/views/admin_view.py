from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Sum
from ..models import Client, Project, Task, Employee, WorkLog
import json 
from decimal import Decimal

# Function to convert Decimal to float
def convert_decimal(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # Convert Decimal to float
    raise TypeError("Type not serializable")
 
def admin_dashboard(request):
    # Pie Chart: Count of Projects per Client
    client_data = list(
        Client.objects.annotate(project_count=Count("project"))
        .values("client_name", "project_count")
    )
    
    # Bar Chart: Tasks per Project
    project_data = list(
        Project.objects.annotate(task_count=Count("task"))
        .values("project_name", "task_count")
    )
    
    # Worklog Chart: Total Hours Logged per Task
    worklog_data = list(
        WorkLog.objects.values("task__task_name")
        .annotate(total_hours=Sum("hours_logged"))
        .order_by("-total_hours")  # Sort by highest hours logged
    )

    context = {
        "client_data": json.dumps(client_data),  # Convert to JSON string
        "project_data": json.dumps(project_data),
        "worklog_data": json.dumps(worklog_data, default=convert_decimal),
    }

    return render(request, "admin_templates/admin_dashboard.html", context)


def admin_clients(request):
    clients = Client.objects.all()
    return render(request, 'admin_templates/admin_clients.html', {'clients': clients})

def admin_projects(request):
    projects = Project.objects.all()
    return render(request, 'admin_templates/admin_projects.html', {'projects': projects})

def admin_tasks(request):
    tasks = Task.objects.all()
    return render(request, 'admin_templates/admin_tasks.html', {'tasks': tasks})

def admin_employees(request):
    employees = Employee.objects.all()
    return render(request, 'admin_templates/admin_employees.html', {'employees': employees})

def admin_work_logs(request):
    work_logs = WorkLog.objects.all()
    return render(request, 'admin_templates/admin_work_logs.html', {'work_logs': work_logs})

def edit_client(request, client_id):
    client = get_object_or_404(Client, client_id=client_id)
    if request.method == 'POST':
        client.client_name = request.POST['client_name']
        client.save()
        return redirect('admin_clients')
    return render(request, 'admin_templates/edit_client.html', {'client': client})


# Admin: Delete a client
def delete_client(request, client_id):
    client = get_object_or_404(Client, client_id=client_id)
    client.delete()
    return redirect('admin_clients')
