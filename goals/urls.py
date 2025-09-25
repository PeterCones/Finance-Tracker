from . import views
from django.urls import path

urlpatterns = [
    path('', views.goals, name='goal'),
]