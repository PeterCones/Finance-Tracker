from . import views
from django.urls import path

urlpatterns = [
    path('add/',views.newTransaction, name='new_transaction'),
    path('add/new-category',views.add_category, name='add_category'),
    path('', views.transaction, name='transaction'),
]