function fetchTasks() {
    const projectSelect = document.getElementById('projectSelect');
    const taskSelect = document.getElementById('taskSelect');
    const projectId = projectSelect.value;

    // Clear the tasks dropdown
    taskSelect.innerHTML = '<option value="">Select task</option>';

    if (projectId) {
        console.log("Selected project ID:", projectId);

        // Make an AJAX request to fetch tasks for the selected project
        fetch(`/employee/get_tasks/?project_id=${projectId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Populate the tasks dropdown
                data.forEach(task => {
                    const option = document.createElement('option');
                    option.value = task.task_id;
                    option.textContent = task.task_name;
                    taskSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error fetching tasks:', error);
            });
    }
}
