from django import forms
from cloudinary.forms import CloudinaryFileField

from .models import User, LostItem, FoundItem


# =================================================
# REGISTER FORM
# =================================================

class RegisterForm(forms.ModelForm):

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm password"
            }
        )
    )

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "mobile",
            "password",
            "confirm_password",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter full name"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter email"
                }
            ),

            "mobile": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter mobile number"
                }
            ),

            "password": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter password",
                    "autocomplete": "new-password"
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    "Password and Confirm Password do not match."
                )

        return cleaned_data


# =================================================
# LOST ITEM FORM
# =================================================

class LostItemForm(forms.ModelForm):

    image = CloudinaryFileField(
        required=False
    )

    class Meta:
        model = LostItem
        fields = [
            "item_name",
            "category",
            "location",
            "lost_date",
            "description",
            "image"
        ]

        widgets = {
            "lost_date": forms.DateInput(
                attrs={"type": "date"}
            )
        }


# =================================================
# FOUND ITEM FORM
# =================================================

class FoundItemForm(forms.ModelForm):

    image = CloudinaryFileField(
        required=False
    )

    class Meta:
        model = FoundItem
        fields = [
            "item_name",
            "category",
            "location",
            "found_date",
            "description",
            "image"
        ]

        widgets = {
            "found_date": forms.DateInput(
                attrs={"type": "date"}
            )
        }

