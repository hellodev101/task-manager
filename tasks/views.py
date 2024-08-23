from datetime import date
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
from psycopg import Transaction
from tasks import services
from .forms import TaskForm, ContactForm 
from .models import Task, Sprint
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from . import services
from django.http import (Http404, HttpRequest, HttpResponse, JsonResponse)
from rest_framework import status

# Task Homepage
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


# Show all task list
class TaskListView(ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"

# Task Detail
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})
    
# Create A new Task
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


# Delete Task
class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:task-list")


# Show Task By List By Date
def task_by_date(request: HttpRequest, by_date: date) -> HttpResponse:
    tasks = services.get_task_by_date(by_date)
    context = {}  # data to inject into the template
    return render(request, "task_list.html", {
        "tasks": tasks
    })


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



def create_task_on_sprint(request, pk):

    """ Create a new task within a sprint"""

    if request.method == "POST":
        task_data: dict[str, str] = {
            "title": request.POST["title"],
            "description": request.POST.get("description", ""),
            "status": request.POST.get("status", "UNASSIGNED"),
        }
        task = services.create_task_and_add_to_sprint(
            task_data, pk, request.user
        )
        return redirect("tasks:task-detail", task_id=task.id)
    raise Http404("Not found")


def claim_task_view(request, task_id):

    """ Once the task has an owner set, nobody else can calim ownership """

    user_id = (request.user.id) 
    try:
        services.claim_task(user_id, task_id)
        return JsonResponse({"message": "Task successfully claimed."})
    except Task.DoesNotExist:
        return HttpResponse("Task does not exist.", status=status.HTTP_404_NOT_FOUND)
    except services.TaskAlreadyClaimedException:
        return HttpResponse("Task is already claimed or completed.", status=status.HTTP_400_BAD_REQUEST)




    

    
    
     
       