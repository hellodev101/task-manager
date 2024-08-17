from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):

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

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})
