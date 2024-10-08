from django import forms
from django.http import Http404
from django.forms import modelformset_factory
from tasks import services
from .models import Task, SubscribedEmail, Sprint
from tasks.validator import EmailListField




class TaskForm(forms.ModelForm):
    watchers = EmailListField(required=False)
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'creator', "watchers"]
    
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # Check if an instance is provided and populate watchers field
        if self.instance and self.instance.pk:
            self.fields['watchers'].initial = ', '.join(email.email for email in self.instance.watchers.all())
    
    def save(self, commit=True):
        # First, save the task instance
        task = super().save(commit)
        # If commit is True, save the associated emails
        if commit:
            # First, remove the old email associated with this task
            task.watchers.all().delete()
            # Add the new emails to the email model
        for email_str in self.cleaned_data["watchers"]:
            SubscribedEmail.objects.create(email=email_str, taks=task)
        return task
    
class ContactForm(forms.Form):
    form_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class SprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ['name', 'description', 'start_date', 'end_date', 'creator', 'tasks', 'epic']
        widgets = {
             'start_date': forms.DateInput(attrs={'type': 'date'}),
             'end_date': forms.DateInput(attrs={'type': 'date'}),
            'tasks': forms.SelectMultiple(),  #  dropdown
        }

        labels = {
            'name': 'Sprint Name',
            'description': 'Sprint Description',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'creator': 'Creator',
            'tasks': 'Select Tasks',
            'epic': 'Related Epic',
        }





