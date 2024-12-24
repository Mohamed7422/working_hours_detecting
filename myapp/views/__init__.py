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
)

from .common_views import(
    home_page
)

 
from .sample_employees import(
    add_sample_employees
)

from .sample_projects import(
    populate_projects
)
from .populate_tasks import(
    populate_tasks
)
