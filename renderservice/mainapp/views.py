import random
import time

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from .models import Task
from .models import Status

from .serializers import TaskSerializer
from .serializers import StatusSerializer


class TaskModelViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self._render(serializer.instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        tasks = Task.objects.filter(user_id=request.user.id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            task = Task.objects.filter(user_id=request.user.id).get(
                id=kwargs['pk'],
            )
            serializer = TaskSerializer(task)
            data = serializer.data
            status_code = status.HTTP_200_OK
        except ObjectDoesNotExist:
            data = {
                'message': f'ERROR: Object with id = {kwargs["pk"]} '
                           f'for user: {request.user.username} does not exist',
            }
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(data=data, status=status_code)

    def _render(self, new_task: Task) -> bool:
        Status(task=new_task, name='rendering').save()
        time.sleep(random.randint(60, 300))
        Status(task=new_task, name='complete').save()
        return True


class StatusModelViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class TaskHistoryRetrieveAPIView(RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        try:
            # TODO: переделать запросы - реализовать одним запросом
            task = Task.objects.filter(user_id=request.user.id).get(
                id=kwargs['pk'],
            )
            task_statuses = Status.objects.filter(task_id=task.id)
            data = {
                'task': TaskSerializer(task).data,
                'status_history': StatusSerializer(
                    task_statuses,
                    many=True,
                ).data,
            }
            status_code = status.HTTP_200_OK
        except ObjectDoesNotExist:
            # TODO: описать ошибку
            data = {
                'message': 'ERROR'
            }
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(data, status=status_code)
