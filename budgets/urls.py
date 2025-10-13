from . import views
from django.urls import path

urlpatterns = [
    path('add/',views.new_budget, name='new_budget'),
    path('edit/<int:budget_id>',views.budget_edit, name='edit_budget'),
    path('delete/<int:budget_id>',views.budget_delete, name='delete_budget'),
    path('', views.budget_list, name='budget'),
]