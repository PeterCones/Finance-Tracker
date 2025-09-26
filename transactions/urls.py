from . import views
from django.urls import path

urlpatterns = [
    path('add/',views.newTransaction, name='new_transaction'),
    # path('',views.TransactionFilterView.as_view(), name='category_transaction'),
    path('', views.transaction, name='transaction'),
]