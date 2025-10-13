from django import forms
from .models import Goal
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Field
from datetime import date


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ("name", "target_amount","saved_amount", "target_date")
        widgets = {
            "target_date": forms.DateInput(attrs={"type": "date"}),
        }
        help_texts = {
            "target_amount": "Enter a positive amount (GBP).",
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        # Placeholders and client-side min date
        if "target_amount" in self.fields:
            self.fields["target_amount"].widget.attrs.update({
                "placeholder": "£0.00",
                "step": "0.01",
                "min": "0",
            })
        if "saved_amount" in self.fields:
            self.fields["saved_amount"].widget.attrs.update({
                "placeholder": "£0.00",
                "step": "0.01",
                "min": "0",
            })
        if "target_date" in self.fields:
            self.fields["target_date"].widget.attrs.update({
                "min": date.today().isoformat(),
            })

        for _, field in self.fields.items():
            field.widget.attrs["class"] = (field.widget.attrs.get("class", "") + " form-control").strip()

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = True
        self.helper.label_class = "form-label"
        self.helper.field_class = ""
        self.helper.form_class = "p-4 border rounded-3 bg-light"

    def clean_target_date(self):
        d = self.cleaned_data.get("target_date")
        if d and d <= date.today():
            raise forms.ValidationError("Please choose a future date.")
        return d
    
    
class IncreaseGoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ("saved_amount",)
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = True
        self.helper.label_class = "form-label"
        self.helper.field_class = ""
        self.helper.form_class = "p-4 border rounded-3 bg-light"


class AdjustGoalForm(forms.Form):
    OP_CHOICES = (("inc", "Increase"), ("dec", "Decrease"))
    operation = forms.ChoiceField(choices=OP_CHOICES, widget=forms.HiddenInput)
    amount = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        max_digits=12,
        widget=forms.NumberInput(attrs={"placeholder": "£0.00", "step": "0.01"})
    )

    def clean_amount(self):
        amt = self.cleaned_data["amount"]
        if amt <= 0:
            raise forms.ValidationError("Enter a positive amount.")
        return amt