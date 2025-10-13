from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Goal
from .forms import GoalForm


class GoalModelTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="erin", password="pw")

	def test_future_date_validation(self):
		g = Goal(
			name="Holiday",
			target_amount=1000,
			saved_amount=100,
			target_date=date.today(),
			owner=self.user,
		)
		with self.assertRaises(ValidationError):
			g.clean()

	def test_days_left_non_negative(self):
		g = Goal(
			name="Laptop",
			target_amount=1000,
			saved_amount=100,
			target_date=date.today() + timedelta(days=10),
			owner=self.user,
		)
		self.assertGreaterEqual(g.days_left, 0)


class GoalViewPermissionTests(TestCase):
	def test_goals_list_requires_login(self):
		res = self.client.get(reverse("goals"))
		self.assertEqual(res.status_code, 302)
		self.assertIn("/accounts/login/", res.url)


class GoalFormValidationTests(TestCase):
	def test_form_rejects_past_date(self):
		form = GoalForm(data={
			"name": "Trip",
			"target_amount": 500,
			"saved_amount": 0,
			"target_date": (date.today() - timedelta(days=1)).isoformat(),
		})
		self.assertFalse(form.is_valid())
		self.assertIn("target_date", form.errors)
