from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [   
    path("", views.index, name="index"),  
    path("new/", views.create_task, name="task-create"),
    path("detail/<int:pk>/", views.task_detail, name="task-detail"),
    path("contact/", views.contact_form, name="contact"), 
    path("contact-success/", views.contact_success, name="contact-success"),  
    
]