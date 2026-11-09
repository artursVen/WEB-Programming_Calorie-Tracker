from django import forms

from .models import FoodEntry


class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodEntry

        fields = (
            "name",
            "quantity_grams",
            "calories_per_100g",
            "meal_type",
            "consumed_at",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Piemēram, auzu pārslas",
                }
            ),
            "quantity_grams": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0.01",
                    "step": "0.01",
                }
            ),
            "calories_per_100g": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                }
            ),
            "meal_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "consumed_at": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["consumed_at"].input_formats = [
            "%Y-%m-%dT%H:%M",
        ]
