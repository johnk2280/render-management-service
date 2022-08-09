from django.contrib import admin

from .models import Task
from .models import Status


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    def display_username(self, obj: Task) -> str:
        return obj.user.username

    def display_status(self, obj: Task) -> str:
        return Status.objects.filter(task_id=obj.pk).latest()

    display_username.short_description = 'Username'
    display_status.short_description = 'Current status'

    list_display = ('display_username', 'name', 'display_status', 'created_at')
    search_fields = ('user__username', 'name', 'statuses__name')
    ordering = ('-created_at',)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    def display_task(self, obj: Status) -> str:
        return obj.task.name

    display_task.short_description = 'Task'

    list_display = ('display_task', 'name', 'created_at')
    search_fields = ('task__name', 'name')
    ordering = ('-created_at', )
