# from django.urls import path, register_converter
from django.urls import path
from . import views
from .views import (TaskListView)

app_name = "tasks"

urlpatterns = [   
    path("", views.index, name="index"),  
    path("new/", views.create_task, name="task-create"),
    path("tasks/", TaskListView.as_view(), name="task-list"),  
    path("detail/<int:pk>/", views.task_detail, name="task-detail"),

    path("contact/", views.contact_form, name="contact"), 
    path("contact-success/", views.contact_success, name="contact-success"),  

    path("new/sprint/", views.create_sprint_view,  name="new-sprint"),
    path("sprints/", views.sprint_list,  name="sprint-list"),
    path("sprint/detail/<int:pk>/", views.sprint_detail,  name="sprint-detail"), 
    
]