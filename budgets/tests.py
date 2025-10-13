from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from budgets.models import Budget
from budgets.views import budget_progress
from transactions.models import Account, Category, Transaction


class BudgetModelTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="alice", password="pw")
		self.cat = Category.objects.create(category="Groceries", is_global=False, owner=self.user)

	def test_budget_saves_and_month_label(self):
		b = Budget.objects.create(
			owner=self.user,
			category=self.cat,
			period_start=date(2025, 1, 1),
			limit_amount=Decimal("100.00"),
		)
		self.assertEqual(b.month_label, "January 2025")

	def test_unique_per_owner_category_month(self):
		Budget.objects.create(
			owner=self.user, category=self.cat, period_start=date(2025, 1, 1), limit_amount=10
		)
		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				Budget.objects.create(
					owner=self.user, category=self.cat, period_start=date(2025, 1, 1), limit_amount=20
				)


class BudgetProgressTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="bob", password="pw")
		self.acc = Account.objects.create(name="NatWest", type="Bank", owner=self.user)
		self.cat = Category.objects.create(category="Groceries", is_global=False, owner=self.user)
		self.budget = Budget.objects.create(
			owner=self.user,
			category=self.cat,
			period_start=date(2025, 10, 1),
			limit_amount=Decimal("100.00"),
		)

		# 2 expenses in month (counted)
		Transaction.objects.create(owner=self.user, description="x", account=self.acc, category=self.cat,
								   type=Transaction.TYPE_EXPENSE, amount=Decimal("10.00"), date=date(2025, 10, 5))
		Transaction.objects.create(owner=self.user, description="y", account=self.acc, category=self.cat,
								   type=Transaction.TYPE_EXPENSE, amount=Decimal("20.00"), date=date(2025, 10, 6))
		# income should not count
		Transaction.objects.create(owner=self.user, description="in", account=self.acc, category=self.cat,
								   type=Transaction.TYPE_INCOME, amount=Decimal("50.00"), date=date(2025, 10, 7))

	def test_budget_progress_spent_remaining_pct(self):
		prog = budget_progress(self.budget)
		self.assertEqual(prog["spent"], Decimal("30.00"))
		self.assertEqual(prog["remaining"], Decimal("70.00"))
		self.assertAlmostEqual(prog["pct"], 30.0, places=1)


class BudgetViewPermissionTests(TestCase):
	def test_budget_list_requires_login(self):
		res = self.client.get(reverse("budget"))
		self.assertEqual(res.status_code, 302)
		self.assertIn("/accounts/login/", res.url)
