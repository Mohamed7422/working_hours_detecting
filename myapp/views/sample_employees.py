from django.shortcuts import render
from ..models import Employee

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
