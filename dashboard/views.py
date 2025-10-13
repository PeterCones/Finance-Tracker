from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage  # add exceptions
from urllib.parse import urlencode
from django.db.models import Sum
from transactions.models import Transaction
from budgets.models import Budget
from goals.models import Goal
from datetime import date, timedelta
from decimal import Decimal


def get_period_end(start):
    # first day of next month
    y, m = start.year, start.month
    if m == 12:
        return date(y + 1, 1, 1)
    return date(y, m + 1, 1)


def budget_progress(budget: Budget) -> dict:
    """
    Compute progress using Transaction.type to identify expenses.
    """
    
    EXPENSE = getattr(Transaction, "TYPE_EXPENSE", "OUT")
    start = budget.period_start.replace(day=1)
    end = get_period_end(start)

    agg = (
        Transaction.objects
        .filter(
            owner=budget.owner,
            category=budget.category,
            date__gte=start, date__lt=end,
            type=EXPENSE,
        )
        .aggregate(total=Sum("amount"))
    )

    spent = agg["total"] or Decimal("0")  # positive number
    limit = budget.limit_amount or Decimal("0")
    pct = (spent / limit * 100) if limit else Decimal("0")
    remaining = limit - spent
    pct_display = float(min(round(pct, 1), 999.9))

    return {
        "spent": spent,
        "limit": limit,
        "remaining": remaining,
        "pct": pct_display,
    }


def _get_page(request, qs, page_param, per_page_default):
    per_page = int(request.GET.get(f'{page_param}_size', per_page_default))
    paginator = Paginator(qs, per_page)
    page_number = request.GET.get(page_param, 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


def _qs_keep(request, exclude_keys):
    return urlencode({k: v for k, v in request.GET.items() if k not in exclude_keys})

@login_required
def index(request):
    user = request.user

    tx_qs = (Transaction.objects
             .filter(owner=user)
             .select_related('account', 'category')
             .order_by('-date'))

    budget_qs = (Budget.objects
                 .filter(owner=user)
                 .order_by('-period_start'))

    goal_qs = (Goal.objects
               .filter(owner=user)
               .order_by('target_date', '-created_at'))

    # paginate querysets
    tx_page     = _get_page(request, tx_qs,     'tx_page',   per_page_default=3)
    budget_page = _get_page(request, budget_qs, 'bdg_page',  per_page_default=1)  # 1 budget per page
    goal_page   = _get_page(request, goal_qs,   'goal_page', per_page_default=1)

    # build progress only for budgets on the current page
    budgets_with_progress = []
    for budget in budget_page:
        progress_data = budget_progress(budget)
        budgets_with_progress.append({"budget": budget, "progress": progress_data})

    context = {
        'tx_page': tx_page,
        'budget_page': budget_page,
        'goal_page': goal_page,
        'budgets_with_progress': budgets_with_progress,  # list for the current page
        'bdg_page': budget_page,                         # use the real paginator for budgets
        'tx_qs':   _qs_keep(request, {'tx_page'}),
        'bdg_qs':  _qs_keep(request, {'bdg_page'}),
        'goal_qs': _qs_keep(request, {'goal_page'}),
    }
    return render(request, 'index.html', context)