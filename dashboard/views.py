from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import F
from transactions.models import Transaction
from budgets.models import Budget
from goals.models import Goal

@login_required
def index(request):
    user = request.user

    # Adjust the user filter to match your models if different (e.g. owner=request.user)
    recent_txns = (
        Transaction.objects
        .filter(owner=request.user)            # change to your FK: e.g. .filter(owner=user)
        .select_related('account', 'category')
        .order_by('-date')[:3]
    )

    featured_budget = (
        Budget.objects
        .filter(owner=request.user)            # change to your FK if needed
        .order_by('-period_start')
        .first()
    )

    # Nearest upcoming goal; fall back to most recently created
    featured_goal = (
        Goal.objects
        .filter(owner=request.user)            # change to your FK if needed
        .order_by('target_date', '-created_at')
        .first()
    )

    return render(request, 'index.html', {
        'recent_txns': recent_txns,
        'featured_budget': featured_budget,
        'featured_goal': featured_goal,
    })