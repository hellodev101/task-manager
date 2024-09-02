from datetime import date, datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import F
from .models import Task, Sprint, User
from django.core.mail import send_mail


def send_contact_email(subject: str, message: str, from_email: str, to_email: str) -> None:
    send_mail(subject, message, from_email, [to_email])


def create_task_and_add_to_sprint(task_data: dict[str, str], sprint_id, creator: User) -> Task:
    """
    Create a new task and associate it with a sprint.
    """
    # Fetch the sprint by its ID
    sprint = Sprint.objects.get(id=sprint_id)

    # Get the current date and time
    # Get the current date
    current_date = datetime.now().date() 
    print("current_date : ", type(current_date ))
    print("current_date : ", current_date)
    print("sprint.start_date: ", type(sprint.start_date))
    print("sprint.start_date: ", sprint.start_date)
    print("sprint.end_date: ", type(sprint.end_date))
    print("sprint.end_date: ", sprint.end_date)

    # Check if the current date and time is within the sprint's start and end dates
    if not (sprint.start_date <= current_date  <= sprint.end_date):
        raise ValidationError("Cannot add task to sprint current date is not within the sprint's start and end dates.")
    with transaction.atomic():
        # Create the task
        task = Task.objects.create(
            title=task_data["title"],
            description=task_data.get("description", ""),
            status=task_data.get("status", "UNASSIGNED"),
            creator=creator,
        )
        # Add the task to the sprint
        sprint.tasks.add(task)
    return task








