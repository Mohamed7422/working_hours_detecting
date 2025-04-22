
from django.shortcuts import render, redirect
from ..models import Employee
from django.urls import reverse
from ..models import  Employee, WorkLog
from datetime import date
from django.http import JsonResponse

def home_page(request):
    return render(request,"main_home.html")
 
def validate_employee(request):
    if request.method == "GET":
        employee_id = request.GET.get("member-id", "").strip() # Retrieve employee ID from request

        # Check if the member ID exists in the database
        if Employee.objects.filter(employee_id=employee_id).exists():
            # Redirect to the 'log_work' view and pass the employee_id as a query parameter
            return redirect('log_work', employee_id=employee_id) # Replace 'log_work' with the name of your check-in page URL
        else:
            # Return to the home page with an error
            return render(request, "main_home.html", {
                "error": "Invalid Member ID. Please try again."
            })
    return render(request, "main_home.html")

# Daily Missing Report
def daily_missing_report(request):
    today = date.today()
    logged_ids = (
        WorkLog.objects
               .filter(date_worked = today)
               .values_list("employee__employee_id", flat=True)
               .distinct()
    )

    missing = Employee.objects.exclude(employee_id__in=logged_ids)
    
    data = [
        {"employee_id": e.employee_id, "name":f"{e.first_name} {e.last_name}"}
        for e in missing
    ]
    return JsonResponse({"missing": data})