from datetime import date, timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

from .forms import budgetForm
from .models import Budget
from transactions.models import Transaction  


def get_period_end(period_start: date) -> date:
    """
    Return the first day of the next month (exclusive end for queries).
    """
    # move to an assuredly-safe day and then to first of next month
    next_month = (period_start.replace(day=28) + timedelta(days=4)).replace(day=1)
    return next_month


def budget_progress(budget: Budget) -> dict:
    """
    Compute progress using Transaction.type to identify expenses.
    """
    start = budget.period_start.replace(day=1)
    end = get_period_end(start)

    agg = (
        Transaction.objects
        .filter(
            owner=budget.owner,
            category=budget.category,
            date__gte=start,
            date__lt=end,
            type=Transaction.TYPE_EXPENSE,  # fixed: use type, not negative amounts
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


@login_required
def budget_list(request):
    """
    List budgets for current user with progress data.
    """
    budgets = (
        Budget.objects.filter(owner=request.user)
        .select_related("category")
        .order_by("-period_start")
    )
    paginator = Paginator(budgets, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    # attach progress to each budget for template rendering
    budgets_with_progress = []
    for budget in page_obj:  # <-- Iterate over the page_obj
        progress_data = budget_progress(budget)
        budgets_with_progress.append({"budget": budget, "progress": progress_data})

    context = {
        "page_obj": page_obj,
        "items_with_progress": budgets_with_progress, # <-- Pass this new list
    }
    return render(request, "budgets.html", context)


@login_required
def new_budget(request):
    if request.method == "POST":
        form = budgetForm(request.POST, user=request.user)
        if form.is_valid():
            b = form.save(commit=False)
            b.owner = request.user
            b.period_start = b.period_start.replace(day=1)
            b.save()
            messages.success(request, "Budget saved.")
            return redirect("budget")  # fixed URL name
        messages.error(request, "Please fix the errors below.")
    else:
        form = budgetForm(user=request.user)

    return render(request, "new_budget.html", {"form": form})
