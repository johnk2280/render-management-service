from rest_framework import serializers

from .models import Task
from .models import Status


class TaskCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Task. Применяется при создании задачи.

    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Task. Применяется при получении списка задач.

    """

    class Meta:
        model = Task
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Status.

    """

    class Meta:
        model = Status
        fields = '__all__'
