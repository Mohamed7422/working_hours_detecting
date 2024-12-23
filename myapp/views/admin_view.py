from django.shortcuts import render, redirect, get_object_or_404
from ..models import Client, Project, Task, Employee, WorkLog
 
    

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
