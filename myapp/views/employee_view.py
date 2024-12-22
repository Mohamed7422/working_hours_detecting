from django.shortcuts import render, redirect, get_object_or_404
from ..models import WorkLog, Task, Employee

def log_work(request):
    if request.method == 'POST':
        # Get input values from the form
        task_name = request.POST['task_name']  # Task name entered by the employee
        date_worked = request.POST['date_worked']
        hours_logged = request.POST['hours_logged']
        is_overtime = 'is_overtime' in request.POST
        comments = request.POST.get('comments', '')

        # Assuming employee is logged in, get the employee object (simplified example)
        employee = Employee.objects.get(employee_id=request.user.id)

        # Create or get the task (optional)
        task, created = Task.objects.get_or_create(task_name=task_name)

        # Create a new WorkLog entry
        WorkLog.objects.create(
            employee=employee,
            task=task,
            date_worked=date_worked,
            hours_logged=hours_logged,
            is_overtime=is_overtime,
            comments=comments
        )
        
        # Redirect to employee work logs after submission
        return redirect('employee_work_logs', employee_id=employee.employee_id)

    return render(request, 'employee_templates/log_work.html')

def employee_work_logs(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    work_logs = WorkLog.objects.filter(employee=employee)
    return render(request, 'employee_templates/employee_work_logs.html', {'work_logs': work_logs, 'employee': employee})
