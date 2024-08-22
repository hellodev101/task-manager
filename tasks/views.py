from django.shortcuts import redirect, render
from django.urls import reverse
from tasks import services
from .models import Task
from .forms import TaskForm, ContactForm 
from .models import Task  
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse


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
    return render(request, "tasks/index.html", context)


# def task_detail(request, pk):
#     try:
#         task = get_object_or_404(Task, pk=pk)
#         return HttpResponse(f"Task: {task.title}, Status: {task.status}")
#     except Http404:
#         return HttpResponse("Task not found.", status=404)
#     except Exception as e:
#         return HttpResponse(f"An error occurred: {str(e)}", status=500)
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})
    

def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()  # Save the new task
            return redirect("tasks:task-detail", task.id)  # Correctly redirect to the task detail page
        else:
            # If the form is not valid, render the form with errors
            return render(request, "tasks/task_form.html", {"form": form})  # Render the form with context
    else:
        form = TaskForm()  # Create an empty form for GET requests

    return render(request, "tasks/task_form.html", {"form": form})  # Render the form with context


# Contact Us
def contact_form(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get("subject")
            message = form.cleaned_data.get("message")
            from_email = form.cleaned_data.get("from_email")
            services.send_contact_email(subject, message, from_email,
                                    ["your-email@example.com"])
            return redirect(reverse("tasks:contact-success"))
        else:
            return render(request, "tasks/contact_form.html", {"form": form})  
    else:
        form = ContactForm()  

    return render(request, "tasks/contact_form.html", {"form": form})  



def contact_success(request):
    return render(request, 'tasks/contact_success.html')
    
    
     
       