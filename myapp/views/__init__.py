from .admin_view import (
    admin_clients,
    admin_projects,
    admin_tasks,
    admin_employees,
    admin_work_logs,
    edit_client,
    delete_client,
)

from .employee_view import (
    log_work,
    employee_work_logs,
    get_tasks_by_project,
    add_task,
    submitEntries,
    get_total_hours,
)

from .common_views import(
    home_page,
    validate_employee
)

 
from .sample_employees import(
    add_sample_employees,
    clickup_task_created
)

from .sample_projects import(
    populate_projects
)
from .populate_tasks import(
    populate_tasks
)
