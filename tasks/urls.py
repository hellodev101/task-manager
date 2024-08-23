from django.urls import path, register_converter
from django.views.generic import TemplateView
from . import views
from .views import (TaskListView)

app_name = "tasks"

urlpatterns = [   
    path("", views.index, name="index"),  
    path("new/", views.create_task, name="task-create"),
    path("detail/<int:pk>/", views.task_detail, name="task-detail"),
    path("contact/", views.contact_form, name="contact"), 
    path("contact-success/", views.contact_success, name="contact-success"),  

    path("tasks/", TaskListView.as_view(), name="task-list"),  #  
    path("tasks/sprint/add_task/<int:pk>/", views.create_task_on_sprint,  name="task-add-to-sprint"),

    
]