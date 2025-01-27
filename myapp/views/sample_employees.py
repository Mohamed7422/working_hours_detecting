from django.shortcuts import render
from ..models import Employee,Project,Client
import json
import requests
from django.http import JsonResponse
from django.db.models import Max
import logging; 
from django.views.decorators.csrf import csrf_exempt
from decouple import Config, RepositoryEnv
import os

# Try loading .env.local if it exists (for local development)
if os.path.exists(".env.local"):
    config = Config(RepositoryEnv(".env.local"))
else:
    # Fall back to system environment variables (e.g., on Vercel)
    config = Config(os.environ)  # Use environment variables for production (e.g., Vercel)
 
CLICKUP_API_TOKEN = config("CLICKUP_API_TOKEN")

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
            project_id = task_details.get("id")

            #Extract the client name
            custom_fields = task_details.get("custom_fields",[])
            client_name = None

            for field in custom_fields:
                if field.get("name")== "Client":
                    client_value_id  = field.get("value")
                    logger.info(f"Extracted client_value_id: {client_value_id}") 
                    
                    if client_value_id is None:
                        continue
                    # Map value ID to client name
                    options = field.get("type_config", {}).get("options", [])
                    logger.info(f"options{options}")
                    for option in options:
                        if option.get("orderindex") == client_value_id:
                            client_name = option.get("name")
                            logger.info(f"client_name from option{client_name}")
                            break


            if not client_name:
                client = Client.objects.filter(client_id="C000").first()
                client_name = client.client_name

            logger.info(f"Extracted client name: {client_name}") 
 
            logger.info(f"Response payload received: {response_payload}")
            logger.info(f"Extracted task name: {task_name}")
 

            # Check if the client exists in the database
            normalized_client_name = client_name.strip().lower()
            logger.info(f"Extracted normalized_client_name {normalized_client_name}")
             
            #normalizing the entries on database
            for client in Client.objects.all():
                client.client_name = client.client_name.strip().lower()
                client.save()

            
            client = Client.objects.filter(client_name__iexact=normalized_client_name).first()
            logger.info(f"Extracted client from DB {client}")
            if not client:
                
                #Generate a unique client_id
                last_client = Client.objects.aggregate(max_id=Max('client_id'))
                last_client_id = last_client['max_id']
                if last_client_id:
                    next_client_id = int(last_client_id[1:])+1 #strip "C" and increment
                    client_id = f"C{next_client_id:03}" #format as "C001"
                else:
                    client_id = "C001"                

                client = Client.objects.create(client_id=client_id, client_name=normalized_client_name)
                logger.info(f"Created new client: {client_name} with ID: {client_id}")
         
          # Retrieve or create a default client
            #default_client_name = "Default Client"  # Replace with your desired default client name
           # default_client, created = Client.objects.get_or_create(
           #     client_name=default_client_name,
            #    defaults={"client_id": client_id}  # Replace with your desired default client ID logic
          #  )
            else:
                logger.info(f"Client already exists: {client.client_name} with ID: {client.client_id}")


            # Generate a unique project_id
            #last_project = Project.objects.aggregate(max_id=Max('project_id'))
            #last_id = last_project['max_id']
            #if last_id:
            #    next_id = int(last_id[1:]) + 1  # Strip "P" and increment
             #   project_id = f"P{next_id:03}"  # Format as "P001"
            #else:
            #    project_id = "P001"  # Start with "P001" if no projects exist


            # Save the project in the database
            Project.objects.create(
                project_id=project_id,
                project_name=task_name,
                client=client
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

@csrf_exempt
def clickup_task_updated(request):

    logger = logging.getLogger('django')
    if request.method == "POST":
        try:

            response_payload = json.loads(request.body)
            logger.info(f"payload recieved: {response_payload}")
            return JsonResponse({"success": True, "message": "Webhook for task update received successfully."})
        except json.JSONDecodeError:
              logger.error("Invalid JSON payload received.")
              return JsonResponse({"success": False, "error": "Invalid JSON payload"}, status=400)
        except Exception as e:    
              logger.error(f"Error processing task update webhook: {str(e)}")      
              return JsonResponse({"success": False, "message": "Invalide request method"},status=405)
    # Invalid HTTP method
    logger.warning("Invalid request method for task update webhook.")
    return JsonResponse({"success": False, "message": "Invalide request method"},status=405)     

@csrf_exempt
def update_project_client(request):
    logger = logging.getLogger('django')
    if request.method == "POST":
        try:
            # Parse the JSON payload
            payload = json.loads(request.body)
            logger.info(f"Payload received: {payload}")

            # Extract the fields
            project_id = payload.get("project_id")
            client_name = payload.get("client_name", "").strip()
            project_name = payload.get("project_name", "").strip()
            logger.info(f"project id , client name, project name {project_id} : {project_name} : {client_name}")

            #get the project from database based on project_id
            project = Project.objects.filter(project_id=project_id).first()
            if not project:
               logger.error(f"Project with ID {project_id} not found.")
               return JsonResponse({"success": False, "message": f"Project with ID {project_id} not found."}, status=404)
              
            #normalize the client name for case-insesitive comparison
            normalized_client_name = client_name.lower()

            #get client from database based on the client_name
            #if not found, create new client but perserve the lower_case
            client = Client.objects.filter(client_name__iexact=normalized_client_name).first()
            if not client:
               #Generate a new unique client_id
               last_client = Client.objects.aggregate(max_id=Max('client_id'))
               last_client_id = last_client['max_id']
               if last_client_id:
                   next_client_id = int(last_client_id[1:])+1 # Strip 'C' and increment
                   client_id = f"C{next_client_id:03}" #Format as "C001"
               else: 
                   client_id = "C000" #no clients exist   

               #create a new client
               client = Client.objects.create(client_id=client_id, client_name=normalized_client_name)     
            else:
                logger.info(f"Client already exists: {client.client_name} with ID: {client.client_id}")

            # Update the project with the new or existing client
            project.client = client
            project.project_name = project_name
            project.save()
            logger.info(f"Updated project {project_id} with client {client.client_name} ({client.client_id})")

            return JsonResponse({"success": True, "message": "Project updated successfully"})

        except json.JSONDecodeError:
            logger.error("Invalid JSON payload")
            return JsonResponse({"success": False, "error": "Invalid JSON payload"}, status=400)
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)         