from django import forms
from .models import Order
import re


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "delivery_type",
            "delivery_date",
            "delivery_time",
            "comment",
        ]
        widgets = {
            "delivery_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "delivery_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
            "delivery_type": forms.Select(attrs={"class": "form-control"}),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Комментарий к доставке",
                }
            ),
        }
        help_texts = {
            "house": "Допустимые форматы: 14к2, 34/2, 12стр5",
            "apartment": "Номер квартиры или офиса",
            "comment": "Любая дополнительная информация",
        }
