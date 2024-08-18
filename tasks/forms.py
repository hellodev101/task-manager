from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'creator']
        # widgets = {
        #     'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        #     'status': forms.Select(),
        #     'owner': forms.Select(),
        # }
        # labels = {
        #     'title': 'Task Title',
        #     'description': 'Task Description',
        #     'status': 'Current Status',
        #     'owner': 'Assign To',
        # }
        # help_texts = {
        #     'title': 'Enter the title of the task.',
        #     'description': 'Provide a detailed description of the task.',
        #     'status': 'Select the current status of the task.',
        #     'owner': 'Choose a user to assign this task to.',
        # }