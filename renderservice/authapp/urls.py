from django.urls import path
from django.urls import include


from .views import UserCreateAPIView


app_name = 'authapp'

urlpatterns = [
    path('', UserCreateAPIView.as_view(), name='registration'),
]
