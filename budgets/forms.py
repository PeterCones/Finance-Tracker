from django import forms
from .models import Budget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Field
from crispy_forms.bootstrap import FormActions
from django.db.models import Q
from datetime import date
from transactions.models import Category  # add

class budgetForm(forms.ModelForm):
    limit_amount = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"placeholder": "£0.00", "step": "0.01"})
    )

    class Meta:
        model = Budget
        fields = ("category", "period_start", "limit_amount")
        widgets = {
            "period_start": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, user=None, **kwargs):  # accept user
        super().__init__(*args, **kwargs)
        self.user = user

        # Determine selected period (first day of month). Default: current month.
        selected = None
        raw = (self.data.get("period_start") if hasattr(self, "data") else None) or self.initial.get("period_start")
        if raw:
            try:
                # raw is like 'YYYY-MM-DD' or a date
                selected = raw if isinstance(raw, date) else date.fromisoformat(str(raw))
            except Exception:
                selected = None
        if not selected:
            selected = date.today()
        selected = selected.replace(day=1)

        # Build category queryset: global or owned by user, excluding already-budgeted categories for that month
        base_qs = Category.objects.all()
        if user and getattr(user, "is_authenticated", False):
            base_qs = base_qs.filter(Q(is_global=True) | Q(owner=user))
            used_ids = (
                Budget.objects.filter(owner=user, period_start=selected)
                .values_list("category_id", flat=True)
            )
            base_qs = base_qs.exclude(id__in=list(used_ids))
        else:
            base_qs = base_qs.filter(is_global=True)

        self.fields["category"].queryset = base_qs.order_by("category")

        # Styling
        for _, field in self.fields.items():
            existing = field.widget.attrs.get("class", "signin-input")
            field.widget.attrs["class"] = f"{existing} form-control".strip()

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = True
        self.helper.label_class = "form-label"
        self.helper.form_class = "p-4 border rounded-3 bg-light"
        self.helper.layout = Layout(
            Row(
                Column(Field("category", css_class="mb-3"), css_class="col-md-4"),
                Column(Field("period_start", css_class="mb-3"), css_class="col-md-4"),
                Column(Field("limit_amount", css_class="mb-3"), css_class="col-md-4"),
                css_class="g-3",
            ),
            FormActions(Submit("submit", "Save Budget", css_class="btn btn-primary w-100 mt-3"))
        )

    def clean(self):
        cleaned = super().clean()
        user = self.user
        cat = cleaned.get("category")
        period = cleaned.get("period_start")
        if user and cat and period:
            period = period.replace(day=1)
            exists = Budget.objects.filter(owner=user, category=cat, period_start=period).exists()
            if exists:
                self.add_error("category", "You already have a budget for this category in the selected month.")
        return cleaned

