from django.shortcuts import render, redirect, get_object_or_404
from ..models import WorkLog, Task, Employee, Project


def log_work(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        project_id = request.POST.get('project_id')
        new_project_name = request.POST.get('new_project_name', '').strip()
        task_id = request.POST.get('task_id')
        new_task_name = request.POST.get('new_task_name', '').strip()
        date_worked = request.POST.get('date_worked')
        hours_logged = request.POST.get('hours_logged')
        is_overtime = request.POST.get('is_overtime') == 'true'
        comments = request.POST.get('comments')

        # Add new project if name is provided
        if new_project_name:
            project, created = Project.objects.get_or_create(
                project_name=new_project_name,
                defaults={'client_id': None}  # Set this based on your logic
            )
            project_id = project.project_id

        # Add new task if name is provided
        if new_task_name:
            task, created = Task.objects.get_or_create(
                task_name=new_task_name,
                defaults={'project_id': project_id}
            )
            task_id = task.task_id

        # Create a work log entry
        WorkLog.objects.create(
            employee_id=employee_id,
            task_id=task_id,
            date_worked=date_worked,
            hours_logged=hours_logged,
            is_overtime=is_overtime,
            comments=comments
        )
        return redirect('home')

    employees = Employee.objects.all()
    projects = Project.objects.all()
    tasks = Task.objects.all()
    return render(request, 'employee_templates/log_work.html', {'employees': employees, 'projects': projects, 'tasks': tasks})

def employee_work_logs(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    work_logs = WorkLog.objects.filter(employee=employee)
    return render(request, 'employee_templates/employee_work_logs.html', {'work_logs': work_logs, 'employee': employee})
