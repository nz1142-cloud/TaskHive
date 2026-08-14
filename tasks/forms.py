from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Bid, Task


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "form-control",
                }
            )


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "category",
            "budget",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter task title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Describe your project...",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "budget": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "Budget",
                }
            ),
        }


class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = [
            "amount",
            "message",
        ]

        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "Your bid amount",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": (
                        "Why are you the best person for this project?"
                    ),
                }
            ),
        }
