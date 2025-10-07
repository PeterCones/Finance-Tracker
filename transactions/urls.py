from . import views
from django.urls import path

urlpatterns = [
    path('add/',views.newTransaction, name='new_transaction'),
    path('edit/<int:transaction_id>',views.transaction_edit, name='edit_transaction'),
    path('delete/<int:transaction_id>',views.transaction_delete, name='delete_transaction'),
    path('', views.transaction, name='transaction'),
]