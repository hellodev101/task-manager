from django.shortcuts import render
from .models import Task

# Create your views here.
def index(request):
    
    #Fetch all tasks using status filter
    tasks = Task.objects.filter(status__in=["UNASSIGNED", "IN_PROGRESS", 
                                            "DONE", "ARCHIVED"])
    # Initialize dictionaries to hold tasks by status
    # context = defaultdict(list)
    context = {
        "unassigned_tasks": [],
        "in_progress_tasks": [],
        "done_tasks": [],
        "archived_tasks": []
    }

    # Categories tasks into their respective lists
    for task in tasks:
        status = task.status.strip().upper()
        if status == "UNASSIGNED":
            print(task.status, "unassigned_tasks")
            context["unassigned_tasks"].append(task)
        elif status == "IN_PROGRESS":
            context["in_progress_tasks"].append(task)
        elif status == "DONE":
            context["done_tasks"].append(task)
        elif status == "ARCHIVED":
            context["archived_tasks"].append(task)
    # render in tasks/home
    return render(request, "tasks/home.html", context)

def task_detail(request):
    return render(request, "tasks/task_detail.html", {
    })