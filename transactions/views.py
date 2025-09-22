from django.shortcuts import render

from django.views import generic
from django.contrib import messages

from django.http import HttpResponseRedirect

from .models import Account, Transaction, Category



# Create your views here.

class TransactionList(generic.ListView):
    queryset = Transaction.objects
    template_name = 'transactions/transactions.html'
    paginate_by = 4