from django.contrib import admin
from tasks.models import Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "status", "owner", "created_at",
                    "updated_at")
    list_filter = ("status",)

admin.site.register(Task, TaskAdmin)