from django.shortcuts import render
from ..models import Employee,Project,Client
import json
import requests
from django.http import JsonResponse
from django.db.models import Max
import logging; 
from django.views.decorators.csrf import csrf_exempt

def add_sample_employees(request):

    
    # Add sample employees
    employees = [
        {"employee_id": "E001", "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "base_hourly_rate": 10.00, "overtime_rate": 12.00},
        {"employee_id": "E002", "first_name": "Jane", "last_name": "Smith", "email": "jane.smith@example.com", "base_hourly_rate": 10.00, "overtime_rate": 12.00},
        {"employee_id": "E003", "first_name": "Alice", "last_name": "Johnson", "email": "alice.johnson@example.com", "base_hourly_rate": 10.00, "overtime_rate": 12.00},
    ]

    for emp in employees:
        Employee.objects.update_or_create(
            employee_id=emp["employee_id"],
            defaults=emp
        )
    return render(request, 'add_employees_success.html')

 # Replace with your actual ClickUp API token
CLICKUP_API_TOKEN = "pk_68545445_Q7B0D6C389GWWG9WSXXK3KZIZ798CTU3"

@csrf_exempt
def clickup_task_created(request):
    logger = logging.getLogger('django')
    if request.method == "POST":
        try:
            # Parse the JSON payload
            response_payload  = json.loads(request.body)
            print("Payload received:", response_payload )
            #  inner_payload = response_payload.get("payload",{})
           # task_name =  inner_payload.get("name", "Unnamed Task") 
            task_id = response_payload.get("task_id")
             # Fetch task details from ClickUp API
            clickup_url = f"https://api.clickup.com/api/v2/task/{task_id}"
            headers = {
                "Authorization": CLICKUP_API_TOKEN,
                "Content-Type": "application/json",
            }
            response = requests.get(clickup_url, headers=headers)

            task_details = response.json()
            logger.info(f"Task details from API: {task_details}")
             
            task_name = task_details.get("name", "Unnamed Task")
 
            logger.info(f"Response payload received: {response_payload}")
            logger.info(f"Extracted task name: {task_name}")


            # Generate a unique project_id
            last_project = Project.objects.aggregate(max_id=Max('project_id'))
            last_id = last_project['max_id']
            if last_id:
                next_id = int(last_id[1:]) + 1  # Strip "P" and increment
                project_id = f"P{next_id:03}"  # Format as "P001"
            else:
                project_id = "P001"  # Start with "P001" if no projects exist
            

            #Generate a unique client_id
            last_client = Client.objects.aggregate(max_id=Max('client_id'))
            last_client_id = last_client['max_id']
            if last_client_id:
                next_client_id = int(last_client_id[1:])+1 #strip "C" and increment
                client_id = f"C{next_client_id:03}" #format as "C001"
            else:
                client_id = "C001"                
          
          # Retrieve or create a default client
            default_client_name = "Default Client"  # Replace with your desired default client name
            default_client, created = Client.objects.get_or_create(
                client_name=default_client_name,
                defaults={"client_id": client_id}  # Replace with your desired default client ID logic
            )
            # Save the project in the database
            Project.objects.create(
                project_id=project_id,
                project_name=task_name,
                client=default_client
            )

            # Save the payload or update the database (if applicable)
            # For example:
            # Task.objects.update_or_create(task_id=task_id, defaults={"name": task_name})

            return JsonResponse({"success": True, "message": f"Webhook processed successfully. Project {task_name} created with ID {project_id}"})
        except json.JSONDecodeError:
             
            return JsonResponse({"success": False, "error": "Invalid JSON payload"}, status=400)
        except Exception as e:
             
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)