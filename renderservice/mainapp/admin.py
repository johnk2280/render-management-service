from django.contrib import admin

from .models import Task
from .models import Status


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Класс для модели Task реализующий отображение списка задач с указанными
    полями на панели администратора.

    """
    def display_username(self, obj: Task) -> str:
        """Метод для реализации отображения имени пользователя.

        :param obj: (Task): объект класса Task.
        :return: (str): имя пользователя.
        """
        return obj.user.username

    def display_status(self, obj: Task) -> str:
        """Метод для реализации отображения статуса.

        :param obj: (Task): объект класса Task.
        :return: (str): статус.
        """
        return Status.objects.filter(task_id=obj.pk).latest()

    display_username.short_description = 'Username'
    display_status.short_description = 'Current status'

    list_display = ('display_username', 'name', 'display_status', 'created_at')
    search_fields = ('user__username', 'name', 'statuses__name')
    ordering = ('-created_at',)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Класс для модели Status реализующий отображение списка задач с указанными
    полями на панели администратора.

    """
    def display_task(self, obj: Status) -> str:
        """Метод для реализации отображения статуса.

        :param obj: (Status): объект класса Status.
        :return: (str): имя задачи.
        """
        return obj.task.name

    display_task.short_description = 'Task'

    list_display = ('display_task', 'name', 'created_at')
    search_fields = ('task__name', 'name')
    ordering = ('-created_at', )
