
from django.shortcuts import render, redirect
from ..models import Employee
from django.urls import reverse


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