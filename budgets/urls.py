from . import views
from django.urls import path

urlpatterns = [
    path('add/',views.newBudget, name='new_budget'),
    path('', views.budget, name='budget'),
]