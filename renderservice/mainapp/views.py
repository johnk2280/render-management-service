import random
import time

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins

from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from rest_framework.permissions import IsAdminUser

from .models import Task
from .models import Status

from .serializers import TaskSerializer
from .serializers import StatusSerializer

from .tasks import render


class TaskModelViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                       mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        # TODO: исправить возможность создание задачи под другим именем
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            render.delay(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        if not request.user.is_staff:
            queryset = queryset.filter(user_id=request.user.id)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            if request.user.is_staff:
                task = self.queryset.get(id=kwargs['pk'])
            else:
                task = self.queryset.filter(user_id=request.user.id).get(
                    id=kwargs['pk'],
                )

            data = self.serializer_class(task).data
            status_code = status.HTTP_200_OK
        except ObjectDoesNotExist:
            data = {
                'message': f'ERROR: Object with id = {kwargs["pk"]} '
                           f'for user: {request.user.username} does not exist',
            }
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(data=data, status=status_code)


class TaskHistoryRetrieveAPIView(RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_staff:
                task = Task.objects.all().get(id=kwargs['pk'])
            else:
                task = Task.objects.filter(user_id=request.user.id).get(
                    id=kwargs['pk'],
                )

            queryset = Status.objects.filter(task_id=task.id)
            data = {
                'task': TaskSerializer(task).data,
                'status_history': StatusSerializer(queryset, many=True).data,
            }
            status_code = status.HTTP_200_OK
        except ObjectDoesNotExist:
            data = {
                'error_message': 'The object with the requested ID is missing.'
            }
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(data, status=status_code)


class StatusModelViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                         mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = (IsAdminUser,)
