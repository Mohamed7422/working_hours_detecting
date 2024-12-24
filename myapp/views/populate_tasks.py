from django.shortcuts import render
from ..models import Task

def populate_tasks(request):
    # Sample task data
    sample_tasks = [
        {"task_id": "T001", "task_name": "UI Mockups", "project_id": "P001"},
        {"task_id": "T002", "task_name": "Backend API", "project_id": "P001"},
        {"task_id": "T003", "task_name": "Marketing Plan", "project_id": "P002"},
        {"task_id": "T004", "task_name": "Enhancements", "project_id": "P001"},
        {"task_id": "T005", "task_name": "User Testing", "project_id": "P003"},
        {"task_id": "T006", "task_name": "Database Setup", "project_id": "P004"},
        {"task_id": "T007", "task_name": "Logo Design", "project_id": "P005"},
        {"task_id": "T008", "task_name": "Content Writing", "project_id": "P002"},
        {"task_id": "T009", "task_name": "Server Configuration", "project_id": "P006"},
        {"task_id": "T010", "task_name": "Analytics Dashboard", "project_id": "P003"},
        {"task_id": "T011", "task_name": "API Documentation", "project_id": "P001"},
        {"task_id": "T012", "task_name": "Product Roadmap", "project_id": "P004"},
        {"task_id": "T013", "task_name": "Security Audit", "project_id": "P006"},
        {"task_id": "T014", "task_name": "Campaign Setup", "project_id": "P003"},
        {"task_id": "T015", "task_name": "Wireframes", "project_id": "P001"},
        {"task_id": "T016", "task_name": "Frontend Development", "project_id": "P004"},
        {"task_id": "T017", "task_name": "Data Migration", "project_id": "P006"},
        {"task_id": "T018", "task_name": "Keyword Research", "project_id": "P005"},
        {"task_id": "T019", "task_name": "Server Maintenance", "project_id": "P004"},
        {"task_id": "T020", "task_name": "System Optimization", "project_id": "P002"},
        {"task_id": "T021", "task_name": "Social Media Posts", "project_id": "P003"},
        {"task_id": "T022", "task_name": "Presentation Design", "project_id": "P001"},
        {"task_id": "T023", "task_name": "Inventory System Setup", "project_id": "P006"},
        {"task_id": "T024", "task_name": "QA Testing", "project_id": "P005"},
        {"task_id": "T025", "task_name": "Bug Fixing", "project_id": "P004"},
        {"task_id": "T026", "task_name": "Meeting Coordination", "project_id": "P003"},
        {"task_id": "T027", "task_name": "Prototyping", "project_id": "P002"},
        {"task_id": "T028", "task_name": "Deployment", "project_id": "P001"},
        {"task_id": "T029", "task_name": "Payment Gateway Integration", "project_id": "P006"},
        {"task_id": "T030", "task_name": "Workshop Planning", "project_id": "P005"},
        {"task_id": "T031", "task_name": "Stakeholder Analysis", "project_id": "P004"},
        {"task_id": "T032", "task_name": "Market Research", "project_id": "P003"},
        {"task_id": "T033", "task_name": "Compliance Review", "project_id": "P002"},
        {"task_id": "T034", "task_name": "Resource Allocation", "project_id": "P001"},
        {"task_id": "T035", "task_name": "Vendor Coordination", "project_id": "P006"},
        {"task_id": "T036", "task_name": "UX Improvements", "project_id": "P003"},
        {"task_id": "T037", "task_name": "Press Release", "project_id": "P005"},
        {"task_id": "T038", "task_name": "Design Updates", "project_id": "P002"},
        {"task_id": "T039", "task_name": "CRM Integration", "project_id": "P004"},
        {"task_id": "T040", "task_name": "Debugging", "project_id": "P001"},
        {"task_id": "T041", "task_name": "Campaign Analysis", "project_id": "P003"},
        {"task_id": "T042", "task_name": "IT Support Planning", "project_id": "P005"},
        {"task_id": "T043", "task_name": "Hosting Setup", "project_id": "P006"},
        {"task_id": "T044", "task_name": "Feature Testing", "project_id": "P004"},
        {"task_id": "T045", "task_name": "Ad Campaign Creation", "project_id": "P002"},
        {"task_id": "T046", "task_name": "Final Presentation", "project_id": "P003"},
        {"task_id": "T047", "task_name": "Post-Launch Support", "project_id": "P001"},
        {"task_id": "T048", "task_name": "Contract Negotiation", "project_id": "P004"},
        {"task_id": "T049", "task_name": "Cloud Backup Configuration", "project_id": "P006"},
        {"task_id": "T050", "task_name": "Review and Feedback", "project_id": "P003"},
        {"task_id": "T1009", "task_name": "New task 2", "project_id": "P000"},
    ]

    # Insert tasks into the database
    for task in sample_tasks:
        Task.objects.update_or_create(
            task_id=task["task_id"],
            defaults={
                "task_name": task["task_name"],
                "project_id": task["project_id"],
            },
        )

    return render(request, "populate_success.html", {"message": "Tasks populated successfully!"})
