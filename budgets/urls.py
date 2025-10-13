from . import views
from django.urls import path

urlpatterns = [
    path('add/',views.new_budget, name='new_budget'),
    path('', views.budget_list, name='budget'),
]