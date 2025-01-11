

// Global variable to store frequently accessed DOM elements
const elements = {
    projectSelect: document.getElementById('projectSelect'),
    taskSelect: document.getElementById('taskSelect'),
    dateInput: document.getElementById('dateWorked'),
    hoursInput: document.getElementById('hoursInput'),
    minutesInput: document.getElementById('minutesInput'),
    commentsInput: document.getElementById('commentsInput'),
    tasksTable: document.getElementById('tasksTable'),
};

function fetchTasks() {

    const projectId = projectSelect.value;

    // Clear the tasks dropdown
    elements.taskSelect.innerHTML = '<option value="">Select task</option>';

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

//set the current date when the form page loads:
document.addEventListener("DOMContentLoaded", function(){
     
           const today = new Date();
           const formmattedDate = today.toISOString().split('T')[0]; // Format as YYYY-MM-DD
           elements.dateInput.value = formmattedDate; //Set the value of the Input
})
 

function addTaskToTable(){
    const dateWorked = elements.dateInput.value;
    const project = elements.projectSelect.options[elements.projectSelect.selectedIndex]?.text;
    const task = elements.taskSelect.options[elements.taskSelect.selectedIndex]?.text;
    const hoursInput = elements.hoursInput.value;
    const minutesInput = elements.minutesInput.value;
    const commentsInput = elements.commentsInput.value;

         // Validate inputs
    if (!dateWorked || !project || !task ) {
        alert("Please fill in all fields before adding an entry.");
        return;
    }
    // Ensure either hours or minutes is provided
    if (!hoursInput && !minutesInput) {
        alert("Please enter at least hours or minutes.");
        return;
    }

    //convert hours and minutes to total hours as a decimal
    const totalHours = parseFloat(hoursInput||0) + (parseFloat(minutesInput || 0) / 60);
    console.log("Total Hours:", totalHours.toFixed(2));

    // Get the table body
    const tableBody = elements.tasksTable.querySelector("tbody");
     
    const selectedProjectId = elements.projectSelect.value;
    const selectedTaskId = elements.taskSelect.value;
     
    // Create a new row
     const newRow = document.createElement("tr");
    newRow.setAttribute("data-project-id",selectedProjectId);
    newRow.setAttribute("data-task-id",selectedTaskId);

 
      // Create table cells
    newRow.innerHTML = `
    <td>${project}</td>
    <td>${task}</td>
    <td>${totalHours.toFixed(1)}</td>
    <td>${commentsInput}</td>
    <td><button class="btn btn-secondary" onclick="deleteRow(this)">Delete</button></td>
`;

     // Append the new row to the table body
     tableBody.appendChild(newRow);
     console.log("Row added:", newRow);

    // Clear form fields
    elements.hoursInput.value = "";
    elements.minutesInput.value = "";
    elements.commentsInput.value = "";
    elements.taskSelect.innerHTML = '<option value="">Select task</option>';
    elements.projectSelect.selectedIndex = 0;

     // Update hours
     updateHours();
 
}

function deleteRow(button) {
    // Remove the row containing the delete button
    const row = button.closest("tr");
    row.remove();
    updateHours();
}


function addNewTaskPrompt(){

   const projectId = elements.projectSelect.value;
   if(!projectId){
    alert("Please select a project before adding a task.");
    return;
   }

   // Show a dialog to get the task name
   const taskName = prompt("Enter the name of the new task:");

   // Validate the input
   if (!taskName) {
       alert("Task name cannot be empty.");
       return;
   }

   // Send the new task to the server
   fetch('/employee/add_task/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(), // Replace with your CSRF token logic
    },
    body: JSON.stringify({
        project_id: projectId,
        task_name: taskName,
    }),
})
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Add the new task to the task dropdown
            const taskSelect = elements.taskSelect;
            const newOption = document.createElement("option");
            newOption.value = data.task_id; // Use the task ID returned by the server
            newOption.textContent = taskName;
            taskSelect.appendChild(newOption); //add new task to the task table

            // Automatically select the new task
            taskSelect.value = data.task_id;

            alert("Task added successfully!");
        } else {
            alert("Failed to add task: " + data.error);
        }
    })
    .catch(error => console.error("Error adding task:", error));

}
 

//Submit All Enteries or Tasks to the database
async function submitEntries() {

    
    const tableBody = elements.tasksTable.querySelector("tbody");

    const rows = tableBody.querySelectorAll("tr");

    const entries = [];
    const addedTasksByDate = {}; // This obj to track added tasks by date
    const hoursLoggedByDate = {} // Object to track total hours logged by date
    const date_worked = elements.dateInput.value;

    //makesure the date worked is exist
    if(!date_worked){
        //alert("Date is required for all tasks.")
        showErrorAlert("Date is required for all tasks.");
        return;
    }

    // Fetch the total hours from backend for the selected date
    const totalHoursFromDB = await fetchTotalHours(date_worked)
    console.log("totalHoursFromDB: ",totalHoursFromDB)
   
    rows.forEach((row) => {
        const cells = row.querySelectorAll("td");
        const projectId = row.getAttribute("data-project-id")
        const taskId  =  row.getAttribute("data-task-id") 
        const hours_logged    = parseFloat(cells[2]?.textContent.trim());
        const comments = cells[3]?.textContent.trim();
          
        //Init the set for specific date if it does not exist
        if(!addedTasksByDate[date_worked]){
            addedTasksByDate[date_worked]= new Set();
            hoursLoggedByDate[date_worked]= totalHoursFromDB; // Initialize with database hours
        }
        
        //check the task id if it's already added for the specific date
        if(addedTasksByDate[date_worked].has(taskId)){
            //alert(`Duplicate task detected for the same day: Task ID ${taskId}. This task will be skipped.`);
            showErrorAlert(`Duplicate task detected for the same day: Task ID ${taskId}. This task will be skipped.`);
            return;
        }

       


        if(projectId && taskId && !isNaN(hours_logged)){
            entries.push({
                project_id: projectId,
                task_id: taskId,
                date_worked: date_worked,
                hours_logged: hours_logged,
                comments: comments,
            });

           addedTasksByDate[date_worked].add(taskId);
           hoursLoggedByDate[date_worked] += hours_logged;
           console.log("Hours: ", hoursLoggedByDate[date_worked])
           console.log("Hours: ", hoursLoggedByDate[date_worked]+ hours_logged)  
           entries == []
        }

         // Check if adding this task exceeds 8 hours for the same date
         if(hoursLoggedByDate[date_worked] + hours_logged > 8){
            console.log("Hours: ", hoursLoggedByDate[date_worked])
            console.warn(
                `Warning: Adding task ID ${taskId} will exceed the 8-hour limit for ${date_worked}.`
            );
            //console.log("Hours: ", hoursLoggedByDate[date_worked] + parseFloat(hours_logged))
            // alert(`Cannot add task name ${taskId}. Adding this task would exceed the 8-hour limit for ${date_worked}.`);
            

             /**To Do */
            //showExceedingHoursAlert(`Be Carful: You are going to exceed the 8-hour standard for ${date_worked}.`);
            showWarningNotification(`Heads up! Logging this task will bring your total hours for ${date_worked} above the standard 8-hour limit.`);
            
        }
        
    });

       // Check if entries array is empty before sending the request
       if (entries.length === 0) {
        //alert("No tasks found to add.");
        showErrorAlert("No tasks found to add.");
        console.error("No entries to submit.");
        return; // Prevent further execution
    }

    // Log the entries array to ensure it's not empty
    console.log("Submitting entries:", entries);


    //Post the data to Django backend
    fetch("/employee/submit_entries/",{
        method: "POST",
        headers:{
            'Content-Type': "application/json",
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({entries}),
    })
    .then((response)=> {
        if(!response.ok){
            return response.json().then((data) => {
                throw data;
            })
            //alert("Something went wrong while submitting your entries. Please check your entries or tasks and try again.");
            //throw new Error("Failed to submit entries");
        }
        return response.json();
    })
    .then((data) => {

        if (data.success) {
           // alert("Entries submitted successfully!");
            showSuccessAlert('Entries Submitted');

            // Optionally clear the table or display a success message
            tableBody.innerHTML ="";

            // Reset hours
           document.getElementById("regularHours").textContent = "0.0";
           document.getElementById("overtimeHours").textContent = "0.0";


        } else {
            //alert(`Error submitting entries: ${data.error || "Unknown error occurred. Please try again."}`);
            showErrorAlert(`Error submitting entries: ${data.error || "Unknown error occurred. Please try again."}`);
        }
    })
    .catch((error) => {
        console.error("Error submitting entries:", error);

            // Handle specific backend error messages
            if (error.error === "No entries provided.") {
                //alert("No entries provided. Please add tasks before submitting.");
                showErrorAlert("No entries provided. Please add tasks before submitting.");
            } else if (error.error) {
                //alert(`Error: ${error.error}`);
                showErrorAlert(`Error: ${error.error}`);
            } else {
                //alert("Something went wrong while submitting your entries. Please try again later.");
                showErrorAlert("Something went wrong while submitting your entries. Please try again later.");
            }
    });
 
    console.log("Entries: ", entries);
    console.log("Test log for debugging");
    
}

//Utility Function for CSRF Token
function getCsrfToken() {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith("csrftoken=")) {
            return cookie.substring("csrftoken=".length, cookie.length);
        }
    }
    return "";
}


//retrieve total hours for the selected date.
async function fetchTotalHours(date_worked) {
    try {
        const response = await fetch(`/employee/get_total_hours?date_worked=${date_worked}`)
        if(!response.ok){
            throw new Error("Failed to fetch total hours.");
        }

        const data =  await response.json();
        console.log("API Response:", data);

        if (data.success) {
            return data.total_hours || 0;
        } else {
            //alert(`Error fetching total hours: ${data.error}`);
            //return 0;
            throw new Error(data.error || "Unknown error occurred while fetching total hours.");
        }
        



    } catch (error) {
        console.error("Error fetching total hours:", error);
        alert(`Unable to fetch total hours. Please try again. Error: ${error.message}`);
        return 0;
    }
    
}

function updateHours() {
    
    const tableBody = elements.tasksTable.querySelector("tbody");

    const rows = tableBody.querySelectorAll("tr");
    let minHours = 8;
    let regularHours = 0; // To track cumulative hours
    let overtimeHours = 0; // To track hours above 8
    
    // Loop through each row in the table to sum up the hours
    rows.forEach((row) => {
        const cells = row.querySelectorAll("td");
        const hoursCell = cells[2];
         if (hoursCell) {
            const hours = parseFloat(hoursCell.textContent.trim()) || 0; // Parse hours

            if(regularHours < minHours){
                const remainingRegularHours = minHours - regularHours;

                if(hours <= remainingRegularHours){
                    regularHours += hours;
                }else{
                    regularHours += remainingRegularHours;
                    overtimeHours += hours - remainingRegularHours;
                }

            }else{
                overtimeHours += hours;
            }
             
        }
    });
    
    // Calculate overtime
   // overtimeHours = regularHours > minHours ? regularHours - minHours : 0;
    
    // Update the DOM
    document.getElementById("regularHours").textContent = regularHours.toFixed(1); // Show total hours
    document.getElementById("overtimeHours").textContent = overtimeHours.toFixed(1); // Show overtime hours
}
