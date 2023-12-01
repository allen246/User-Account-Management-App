from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import User
from django.contrib.auth.forms import PasswordResetForm
from user_management.tasks import send_mail


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class SignUpForm(UserCreationForm):
    phone_validator = RegexValidator(
        regex=r"^\+?[0-9]+$",
        message="Enter a valid phone number (only integers and + symbol are allowed).",
        code="invalid_phone",
    )

    username = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    role = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    country = forms.ChoiceField(
        choices=User.COUNTRY_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    nationality = forms.ChoiceField(
        choices=User.NATIONALITY_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    mobile = forms.CharField(
        max_length=15,
        required=True,
        validators=[phone_validator],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "country",
            "nationality",
            "role",
        )


class RecoverPasswordForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control"}))

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        context["user"] = context["user"].id

        send_mail.delay(
            subject_template_name=subject_template_name,
            email_template_name=email_template_name,
            context=context,
            from_email=from_email,
            to_email=to_email,
            html_email_template_name=html_email_template_name,
        )


class ConfirmPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
