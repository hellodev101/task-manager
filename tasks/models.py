from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class VersionMixing:
    version = models.IntegerField(default=0)

class Task(models.Model):
    """ Task: A unit of work that needs to be completed, which can be assigned to team members."""
    STATUS_CHOICES = [
        ("UNASSIGNED", "Unassigned"),
        ("IN_PROGRESS", "In Progress"),
        ("DONE", "Completed"),
        ("ARCHIVED", "Archived"),
    ]

    title = models.CharField(max_length=200)
    # in the form can be blank, but in db can't be null
    description = models.TextField(blank=True, 
                                   null=False, 
                                   default="")
    status = models.CharField(max_length=200, 
                              choices=STATUS_CHOICES, 
                              default="UNASSIGNED",
                              db_comment="Can be UNASSIGNED, IN_PROGRESS, DONE, or ARCHIVED.",)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, 
                                related_name="created_tasks", 
                                on_delete=models.CASCADE)
    # One user can have many tasks
    owner = models.ForeignKey(User, 
                              related_name="owned_tasks", 
                              on_delete=models.SET_NULL, 
                              null=True)
    

# create constraint status_check on model Task
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(status="UNASSIGNED")|
                    models.Q(status='IN_PROGRESS') | 
                    models.Q(status='DONE')|
                    models.Q(status='ARCHIVED'),
                    name='status_check'
            ),
        ]
    
    def __str__(self):
        return f"{str(self.title)}, {str(self.status)}, {str(self.owner)}"
    

    def get_absolute_url(self):
        return reverse("tasks:task-detail", kwargs={"pk": self.pk})


class SubscribedEmail(models.Model):
    email = models.EmailField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, 
                             related_name="watchers")


class Sprint(models.Model):
    """Sprint: A defined period during which specific work has to be completed and made ready for review."""

    # TODO: Define fields here
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User,
                                related_name="created_sprints",
                                  on_delete=models.CASCADE)
    # one task could be into one or more sprints and vice versa
    tasks = models.ManyToManyField('Task', related_name='sprints', blank=True)
    epic = models.ForeignKey('Epic', 
                             related_name='sprints',
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(end_date__gt=models.F('start_date')),
                                   name='end_date_after_start_date'),
        ]

    def __str__(self):
        return f"{self.name} (ID: {self.id}, {self.start_date}, {self.end_date})"
    
    def get_absolute_url(self):
        return reverse("tasks:sprint-detail", kwargs={"pk": self.pk})

class Epic(models.Model):
    """Model definition for MODELNAME."""

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, 
                                related_name='created_epics',
                                on_delete=models.CASCADE)
