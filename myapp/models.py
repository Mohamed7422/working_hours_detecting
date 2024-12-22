 

# Create your models here.
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    from django.db import models

class Client(models.Model):
    client_id = models.CharField(max_length=10, primary_key=True)
    client_name = models.CharField(max_length=100)

    def __str__(self):
        return self.client_name


class Project(models.Model):
    project_id = models.CharField(max_length=10, primary_key=True)
    project_name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.project_name


class Task(models.Model):
    task_id = models.CharField(max_length=10, primary_key=True)
    task_name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name


class Employee(models.Model):
    employee_id = models.CharField(max_length=10, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    base_hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    overtime_rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class WorkLog(models.Model):
    work_log_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date_worked = models.DateField()
    hours_logged = models.DecimalField(max_digits=5, decimal_places=2)
    is_overtime = models.BooleanField(default=False)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"WorkLog {self.work_log_id} - {self.employee}"
