import time
import random

from renderservice.celery import app

from .models import Status
from .models import Task


@app.task
def render(task_id: int) -> bool:
    """Функция имитирующая работу по отрисовке изображения.

    :param task_id: (int): Атрибут `id` объекта класса Task.
    :return: (bool):

    """
    new_task = Task.objects.get(id=task_id)
    Status(task=new_task, name='rendering').save()
    time.sleep(random.randint(60, 300))
    Status(task=new_task, name='complete').save()
    return True
