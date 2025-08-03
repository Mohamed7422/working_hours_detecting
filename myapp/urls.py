from django.urls import path
from django.http import HttpResponse
 
#def home(request):
    #return HttpResponse("<h1>Welcome to the Application</h1><p>Please navigate to /admin or /employee.</p>")


from .views import (
    home_page,
    validate_employee,
    admin_dashboard,
    admin_clients,
    admin_projects,
    admin_tasks,
    admin_employees,
    admin_work_logs,
    edit_client,
    delete_client,
    log_work,
    employee_work_logs,
    get_tasks_by_project,
    add_task,
    submitEntries,
    get_total_hours,
    add_sample_employees,
    populate_projects,
    populate_tasks,
    clickup_task_created,
    clickup_task_updated,
    update_project_client,
    daily_missing_report,
    daily_worklog_view
     
)

urlpatterns = [

     # Home URL (default)
    #path('', home, name='home'),  # Add this line for the root URL

    path('',home_page, name='home_page'),
    path('validate_employee/',validate_employee, name='validate_employee'),

    path('add-sample-employees/', add_sample_employees, name='add_sample_employees'),
    path("daily_missing_report/", daily_missing_report, name="daily_missing_report"),

    path("populate-projects/", populate_projects, name="populate_projects"),
    path("populate-tasks/", populate_tasks, name="populate_tasks"),
    path("populate-projectcreated/", clickup_task_created, name="clickup_task_created"),
    path("populate-projectupdated/", clickup_task_updated, name="clickup_task_updated"),
    path("populate-clientupdated/", update_project_client, name="update_project_client"),

    


    # Admin URLs
    path("customizeddashboard/", admin_dashboard, name="admin_dashboard"),
    path('admin/clients/', admin_clients, name='admin_clients'),
    path('admin/projects/', admin_projects, name='admin_projects'),
    path('admin/tasks/', admin_tasks, name='admin_tasks'),
    path('admin/employees/', admin_employees, name='admin_employees'),
    path('admin/work_logs/', admin_work_logs, name='admin_work_logs'),
    path('admin/edit_client/<str:client_id>/', edit_client, name='edit_client'),
    path('admin/delete_client/<str:client_id>/', delete_client, name='delete_client'),

    # Employee URLs
    path('employee/log_work/<str:employee_id>/', log_work, name='log_work'),
    path('employee/work_logs/<str:employee_id>/', employee_work_logs, name='employee_work_logs'),
    path('employee/get_tasks/', get_tasks_by_project, name='get_tasks_by_project'),
    path('employee/add_task/', add_task, name='add_task'),
    path('employee/submit_entries/',submitEntries,name= 'submitEntries'),
    path('employee/get_total_hours/', get_total_hours, name='get_total_hours'),
    

    #Report URLs
    path('daily-worklogs/', daily_worklog_view, name='daily_worklogs'),

]
