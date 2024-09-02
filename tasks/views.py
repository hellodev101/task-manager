from datetime import date
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
from psycopg import Transaction
from . import services
from tasks import services
from .forms import TaskForm, ContactForm, SprintForm
from .models import Task, Sprint
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from django.http import (Http404, HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse)
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages



@login_required
def index(request):
       
    #Fetch all tasks using status filter
    tasks = Task.objects.filter(status__in=["UNASSIGNED", "IN_PROGRESS", 
                                            "DONE", "ARCHIVED"])
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
@login_required
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


@login_required 
def create_task_on_sprint(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    sprint_id = get_object_or_404(Sprint, pk=pk)  # Ensure the sprint exists
    

    if request.method == "POST":
        title = request.POST.get("title")
        if not title:
            raise Http404("Title is required")  # Validate title presence

        task_data: dict[str, str] = {
            "title": title,
            "description": request.POST.get("description", ""),
            "status": request.POST.get("status", "UNASSIGNED"),
        }
        user = request.user
        task = services.create_task_and_add_to_sprint(task_data, sprint_id, user)
        return redirect("tasks:task-detail", task.id)
    
    raise Http404("Not found")


@login_required 
def create_sprint_view(request):
    if request.method == "POST":
        form = SprintForm(request.POST)
        if form.is_valid():
            sprint = form.save()  # Save the new task
            return redirect("tasks:sprint-detail", sprint.id)
        else:
            # If the form is not valid, render the form with errors
            return render(request, "tasks/sprint_form.html", {"form": form})  
    else:
        form = SprintForm()  # Create an empty form for GET requests

    return render(request, "tasks/sprint_form.html", {"form": form})  


def sprint_list(request):
    sprints = Sprint.objects.all()
    return render(request, "tasks/sprint_list.html", {
        "sprints": sprints
    })

def sprint_detail(request, pk):
    sprint = get_object_or_404(Sprint, pk=pk)    
    tasks = Task.objects.filter(sprints__id=pk)

    if request.method == 'POST': 
        title = request.POST.get("title")
        description = request.POST.get("task-description")
        status = request.POST.get("status", "UNASSIGNED")
        
        task_data: dict[str, str] = {
            "title": title,
            "description": description,
            "status": status
        }
        user = request.user
        
        try:
            task = services.create_task_and_add_to_sprint(task_data, sprint.id, user)
            return redirect('tasks:index')  # Redirect to the same sprint detail page
        except Exception as error:
            messages.error(request, str(error))  # Capture the exception message
            print(error, "error message")
            return render(request, 'tasks/sprint_detail.html', 
                  {'sprint': sprint,
                   'tasks': tasks,
                   'error': error
                   })

    return render(request, 'tasks/sprint_detail.html', 
                  {'sprint': sprint,
                   'tasks': tasks,
                   })
    


# def remove_task_view(request, sprint_id, task_id):
#     remove_task_from_sprint(sprint_id, task_id)
#     return JsonResponse({'status': 'success'})


# def set_sprint_epic_view(request, sprint_id, epic_id):
#     set_sprint_epic(sprint_id, epic_id)
#     return JsonResponse({'status': 'success'})






    

    
    
     
       