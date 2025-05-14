from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["delivery_type", "delivery_date", "delivery_time", "address"]
        widgets = {
            "delivery_date": forms.DateInput(attrs={"type": "date"}),
            "delivery_time": forms.TimeInput(attrs={"type": "time"}),
            "address": forms.Textarea(attrs={"rows": 3}),
        }
