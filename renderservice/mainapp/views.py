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
    """Представление реализующее отображение списка задач, создание новой
    задачи и получение детальной информации о задаче по ее `id`.

    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        """Переопределенный метод класса CreateModelMixin для
        десериализации объекта класса Task и записи его в БД.

        :param request: (Request): объект класса rest_framework.request.Request.
        :param args: дополнительные параметры объекта класса Request.
        :param kwargs: дополнительные параметры объекта класса Request.
        :return: (Response): В случае успешного выполнения возвращает
                объект класса Response с указанием параметров вновь созданного
                объекта класса Task и статус-кода 201.
                В противном случае возвращает в объекте Response
                сообщение c описанием ошибки и статус-код 400.

        """
        serializer = self.serializer_class(data=request.data)
        # TODO: исправить возможность создание задачи под другим именем пользователя
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            render.delay(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """Переопределенный метод класса ListModelMixin для
        получения списка объектов класса Task по `id` пользователя.

        :param request: (Request): объект класса rest_framework.request.Request.
        :param args: дополнительные параметры объекта класса Request.
        :param kwargs: дополнительные параметры объекта класса Request.
        :return: (Response): В случае успешного выполнения возвращает
                объект класса Response с указанием списка объектов класса Task
                и статус-кода 200.

        """
        queryset = self.queryset
        if not request.user.is_staff:
            queryset = queryset.filter(user_id=request.user.id)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """Переопределенный метод класса RetrieveModelMixin для
        получения детальной информации объекта класса Task по
        `id` пользователя и`id` задачи.

        :param request: (Request): объект класса rest_framework.request.Request.
        :param args: дополнительные параметры объекта класса Request.
        :param kwargs: дополнительные параметры объекта класса Request.
        :return: (Response): В случае успешного выполнения возвращает
                объект класса Response с указанием списка объектов класса Task
                и статус-кода 200.
                В противном случае возвращает в объекте Response
                сообщение c описанием ошибки и статус-код 400.

        """
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
    """Представление реализующее получение истории смены статусов по `id` задачи.

    """

    def get(self, request, *args, **kwargs):
        """Метод обработки GET запроса дял получения истории смены статусов
        задачи по `id` пользователя и `id` задачи.

        :param request: (Request): объект класса rest_framework.request.Request.
        :param args: дополнительные параметры объекта класса Request.
        :param kwargs: дополнительные параметры объекта класса Request.
        :return: (Response): В случае успешного выполнения возвращает
                объект класса Response с указанием детальной информации о
                задаче и списка статусов с указанием деталей и статус-кода 200.
                В противном случае возвращает в объекте Response
                сообщение c описанием ошибки и статус-код 400.

        """
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
    """Представление реализующее получение списка статусов по всем задачам."""

    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = (IsAdminUser,)
