from django.shortcuts import render
from ..models import Project

def populate_projects(request):
    # Sample project data
    sample_projects = [
        {"project_id": "P001", "project_name": "Website Redesign", "client_id": "C001"},
        {"project_id": "P002", "project_name": "Mobile App Launch", "client_id": "C002"},
        {"project_id": "P003", "project_name": "Marketing Campaign", "client_id": "C003"},
        {"project_id": "P004", "project_name": "E-commerce Development", "client_id": "C004"},
        {"project_id": "P005", "project_name": "CRM System Implementation", "client_id": "C005"},
        {"project_id": "P006", "project_name": "Data Analytics Setup", "client_id": "C006"},
        {"project_id": "P007", "project_name": "Social Media Strategy", "client_id": "C001"},
        {"project_id": "P008", "project_name": "Cloud Migration", "client_id": "C002"},
        {"project_id": "P009", "project_name": "Brand Identity Creation", "client_id": "C003"},
        {"project_id": "P010", "project_name": "Custom Software Development", "client_id": "C004"},
        {"project_id": "P011", "project_name": "IT Infrastructure Upgrade", "client_id": "C005"},
        {"project_id": "P012", "project_name": "SEO Optimization", "client_id": "C006"},
        {"project_id": "P000", "project_name": "No Project", "client_id": "C000"},
    ]

    # Insert projects into the database
    for project in sample_projects:
        Project.objects.update_or_create(
            project_id=project["project_id"],
            defaults={
                "project_name": project["project_name"],
                "client_id": project["client_id"],
            },
        )

    return render(request, "populate_success.html", {"message": "Projects populated successfully!"})
