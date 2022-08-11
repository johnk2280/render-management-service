import datetime

from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    """Класс модели задач."""

    user = models.ForeignKey(
        User,
        related_name='tasks',
        verbose_name='User',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name='Task name',
        max_length=128,
        unique=True,
        null=False,
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name='Created at',
        auto_now_add=True,
    )

    class Meta:
        db_table = 'tasks'
        ordering = ('-created_at',)
        verbose_name = 'task'
        verbose_name_plural = 'tasks'

    def __str__(self):
        return self.name

    def _set_default_task_name(self):
        self.name = f'task_{self.user.username}_{datetime.datetime.now()}'

    def save(self, *args, **kwargs):
        if not self.name:
            self._set_default_task_name()

        super(Task, self).save(*args, **kwargs)
        status = Status(task=self)
        status.save()


class Status(models.Model):
    """Класс модели статусов."""

    CREATE = 'create'
    RENDERING = 'rendering'
    COMPLETE = 'complete'

    STATUS_CHOICES = (
        (CREATE, 'CREATE'),
        (RENDERING, 'RENDERING'),
        (COMPLETE, 'COMPLETE'),
    )

    task = models.ForeignKey(
        Task,
        related_name='statuses',
        verbose_name='Task',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name='Status name',
        max_length=9,
        choices=STATUS_CHOICES,
        default=CREATE,
    )
    created_at = models.DateTimeField(
        verbose_name='Created at',
        auto_now_add=True,
    )

    class Meta:
        db_table = 'statuses'
        ordering = ('-created_at',)
        get_latest_by = ('created_at',)
        verbose_name = 'status'
        verbose_name_plural = 'statuses'

    def __str__(self):
        return self.name
