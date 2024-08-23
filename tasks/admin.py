from django.contrib import admin
from tasks.models import Task, Sprint

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "status", "owner", "created_at",
                    "updated_at")
    list_filter = ("status",)

admin.site.register(Task, TaskAdmin)


class SprintAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "start_date", "end_date", "created_at",
                    "updated_at")
    list_filter = ("start_date",)

admin.site.register(Sprint, SprintAdmin)