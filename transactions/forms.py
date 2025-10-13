from django import forms
from .models import Transaction, Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Field 

class TransactionForm(forms.ModelForm):
    amount = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "placeholder": "£0.00",
            "step": "0.01",
        })
    )

    class Meta:
        model = Transaction
        fields = ("amount", "description","account", "category","type", "date")
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            # If these are FKs, Select is fine; add classes via Field below
            # "account": forms.Select(),
            # "category": forms.Select(),
        }
        help_texts = {
            "amount": "Enter a positive amount (GBP).",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Optional: set default CSS classes on all fields
        for name, field in self.fields.items():
            # Append rather than replace to keep any widget defaults
            existing = field.widget.attrs.get("class", "signin-input")
            field.widget.attrs["class"] = f"{existing} form-control".strip()

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = True
        self.helper.label_class = "form-label"
        self.helper.field_class = ""  # let Bootstrap’s grid do the spacing
        self.helper.form_class = "p-4 border rounded-3 bg-light"

        self.helper.layout = Layout(
            Row(
                Column(Field("amount", css_class="mb-3"), css_class="col-md-4"),
                Column(Field("account", css_class="mb-3"), css_class="col-md-4"),
                Column(Field("category", css_class="mb-3"), css_class="col-md-4"),
                css_class="g-3",
            ),
            Row(
                Column(Field("description", css_class="mb-3"), css_class="col-md-6"),
                Column(Field("type", css_class="mb-3"), css_class="col-md-6"),
                css_class="g-3",
            ),
            Row(
                Column(Field("date", css_class="mb-3"), css_class="col-md-12"),
                css_class="g-3",
            ),
            FormActions(
                Submit("submit", "Save Transaction", css_class="btn btn-primary w-100 mt-3")
            )
        )
        


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category',)  # adjust based on your Category model
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }
