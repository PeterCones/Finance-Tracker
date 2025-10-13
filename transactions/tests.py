from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Account, Category, Transaction
from .forms import TransactionForm


class TransactionModelTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="carol", password="pw")
		self.acc = Account.objects.create(name="Wallet", type="Cash", owner=self.user)
		self.cat = Category.objects.create(category="Food", is_global=False, owner=self.user)

	def test_transaction_saves(self):
		t = Transaction.objects.create(
			owner=self.user,
			description="Lunch",
			account=self.acc,
			category=self.cat,
			type=Transaction.TYPE_EXPENSE,
			amount=Decimal("12.50"),
			date=date(2025, 10, 10),
		)
		self.assertEqual(str(t.account.name), "Wallet")
		self.assertEqual(t.amount, Decimal("12.50"))


class TransactionPermissionTests(TestCase):
	def test_transactions_list_requires_login(self):
		res = self.client.get(reverse("transaction"))
		self.assertEqual(res.status_code, 302)
		self.assertIn("/accounts/login/", res.url)


class TransactionFormValidationTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="dave", password="pw")
		self.acc = Account.objects.create(name="Card1", type="Card", owner=self.user)
		self.cat = Category.objects.create(category="Bills", is_global=False, owner=self.user)

	def test_invalid_negative_amount(self):
		form = TransactionForm(
			data={
				"amount": -1,
				"description": "Test",
				"account": self.acc.id,
				"category": self.cat.id,
				"type": Transaction.TYPE_EXPENSE,
				"date": "2025-10-10",
			},
			user=self.user,
		)
		self.assertFalse(form.is_valid())
		self.assertIn("amount", form.errors)

	def test_missing_required_fields(self):
		form = TransactionForm(data={}, user=self.user)
		self.assertFalse(form.is_valid())
		# amount and date should be required at minimum
		self.assertIn("amount", form.errors)
		self.assertIn("date", form.errors)
