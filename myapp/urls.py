from django.urls import path
from django.http import HttpResponse
 
def home(request):
    return HttpResponse("<h1>Welcome to the Application</h1><p>Please navigate to /admin or /employee.</p>")


from .views import (
    admin_clients,
    admin_projects,
    admin_tasks,
    admin_employees,
    admin_work_logs,
    edit_client,
    delete_client,
    log_work,
    employee_work_logs,
)

urlpatterns = [

     # Home URL (default)
    path('', home, name='home'),  # Add this line for the root URL
    # Admin URLs
    path('admin/clients/', admin_clients, name='admin_clients'),
    path('admin/projects/', admin_projects, name='admin_projects'),
    path('admin/tasks/', admin_tasks, name='admin_tasks'),
    path('admin/employees/', admin_employees, name='admin_employees'),
    path('admin/work_logs/', admin_work_logs, name='admin_work_logs'),
    path('admin/edit_client/<str:client_id>/', edit_client, name='edit_client'),
    path('admin/delete_client/<str:client_id>/', delete_client, name='delete_client'),

    # Employee URLs
    path('employee/log_work/', log_work, name='log_work'),
    path('employee/work_logs/<str:employee_id>/', employee_work_logs, name='employee_work_logs'),
]
