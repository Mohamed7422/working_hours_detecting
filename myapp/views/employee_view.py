import json
from decimal import Decimal
from django.utils.dateparse import parse_date
from django.shortcuts import render, redirect, get_object_or_404
from ..models import WorkLog, Task, Employee, Project
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db.models import Sum
 

def get_tasks_by_project(request):
    project_id = request.GET.get('project_id')  # Get the project ID from the query parameter
    if project_id:
        # Query tasks related to the project
        tasks = Task.objects.filter(project_id=project_id).values('task_id', 'task_name')
        return JsonResponse(list(tasks), safe=False)  # Return the tasks as JSON
    return JsonResponse({'error': 'Invalid project ID or no project selected'}, status=400)



def log_work(request):
    employee_id = request.GET.get("member-id")
 
    request.session["employee_id"] = employee_id
    print("Emp ", employee_id)    
    '''if request.method == 'POST':
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
       
        return redirect('home')'''

    employees = Employee.objects.all()
    projects = Project.objects.all()
    tasks = Task.objects.all()
    return render(request, 'employee_templates/log_work.html', {'employees': employees, 'projects': projects, 'tasks': tasks})
  


def submitEntries(request):
    if request.method == "POST":
      try:
          import json

          data = json.loads(request.body)
          employee_id = request.session.get("employee_id")
          entries =  data.get("entries",[]) 
          print("employee_id: ",employee_id)
          print("entries: ",entries)

          if not entries:
              return JsonResponse({
                  'success':False,
                  'error': "No entries provided."
              }, status = 400)
          

          try:
              employee_obj = Employee.objects.get(pk=employee_id)
          except Employee.DoesNotExist:
              return JsonResponse({
                  'success': False,
                  'error':f"Employee with id {employee_id} does not exist."
              },status=400)   
           

          for entry in entries:
              project_id =entry['project_id']
              task_id =  entry['task_id']
              date_str = entry['date_worked']
              hours_str = entry['hours_logged']
              comments = entry['comments']

              date_worked = parse_date(date_str)
              if not date_worked:
                    return JsonResponse({
                        'success': False,
                        'error': f"Invalid date format: {date_str}"
                    }, status=400)
              
              hours_logged = None
              try:
                    hours_logged = Decimal(hours_str)
              except Exception:
                    return JsonResponse({
                        'success': False,
                        'error': f"Invalid number for hours_logged: {hours_str}"
                    }, status=400)
              
              try:
                    task_obj = Task.objects.get(pk=task_id)
              except Task.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': f"Task with id {task_id} does not exist."
                    }, status=400)
              
              #Check for duplicate entry
              if WorkLog.objects.filter(
                  employee_id = employee_obj,
                  task_id = task_id,
                  date_worked = date_worked
              ).exists():
                  return JsonResponse({
                      'success':False,
                      'error': f"Duplicate entry detected for Task Name {task_obj} on {date_worked}."
                  }, status = 400)
              
              #Check task existence
              try:
                  task_obj = Task.objects.get(pk=task_id)
              except Task.DoesNotExist:
                  return JsonResponse({
                      'success': False,
                      'error': f"Task with id {task_id} does not exist."
                  }, status=400)    

              WorkLog.objects.create(
                employee = employee_obj,
                task = task_obj,
                date_worked =date_worked,
                hours_logged = hours_logged,
                comments = comments,  
              )    
          return JsonResponse({'success':True})
      except Exception as e:
           print(e)
           return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

def employee_work_logs(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    work_logs = WorkLog.objects.filter(employee=employee)
    return render(request, 'employee_templates/employee_work_logs.html', {'work_logs': work_logs, 'employee': employee})


#define the end-point
def add_task(request):
    if request.method == "POST":
        try:
           
            data = json.loads(request.body)

            project_id = data.get("project_id")
            task_name = data.get("task_name")

            if not project_id or not task_name:
                return JsonResponse({"success": False, "error": "Missing project ID or task name."}, status=400)

            # Ensure the project exists
            try:
                project = Project.objects.get(project_id=project_id)
            except Project.DoesNotExist:
                return JsonResponse({"success": False, "error": "Project not found."}, status=404)

            # Validate task name
            task_name = task_name.strip()
            if not task_name:
                return JsonResponse({"success": False, "error": "Task name cannot be blank."}, status=400)

            # Generate task ID
            task_id = f"T{str(Task.objects.count() + 1).zfill(3)}"
            if len(task_id) > 10:
                return JsonResponse({"success": False, "error": "Generated task ID is too long."}, status=500)

            # Create task
            new_task = Task.objects.create(
                task_id=task_id,
                task_name=task_name,
                project=project,
            )

            return JsonResponse({"success": True, "task_id": new_task.task_id}, status=201)

        except ValidationError as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)


def get_total_hours(request):
    if request.method == "GET":
        try:
            employee_id = request.session.get("employee_id")
            date_str = request.GET.get("date_worked", None)
            print("EmployeeFromView: ", employee_id)
            print("date Worked: ", date_str)
            if not date_str:
                return JsonResponse({
                    "success": False,
                    "error": "Date is required."
                }, status=400)
            
            date_worked = parse_date(date_str)

            if not date_worked:
                return JsonResponse({
                    "success": False,
                    "error": f"Invalid date format: {date_str}"
                }, status=400)
            
            #Calculate total logged hours

            total_hours = WorkLog.objects.filter(
                employee_id = employee_id,
                date_worked = date_worked
            ).aggregate(total_hours=Sum("hours_logged"))["total_hours"] or 0

            return JsonResponse({
                "success": True,
                "total_hours": total_hours
            })

        except Exception as e:
            return JsonResponse ({"success": False,"error": str(e) },status = 400)
    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)
 
'''

        employee_id = request.POST.get('employee_id')
        project_id = request.POST.get('project_id')
        new_project_name = request.POST.get('new_project_name', '').strip()
        task_id = request.POST.get('task_id')
        new_task_name = request.POST.get('new_task_name', '').strip()
        date_worked = request.POST.get('date_worked')
        hours_logged = request.POST.get('hours_logged')
        is_overtime = request.POST.get('is_overtime') == 'true'
        comments = request.POST.get('comments')

        print("employee_id ",employee_id)

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
    tasks = Task.objects.all() '''
