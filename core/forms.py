from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import User
from user_service.models import Customer, Service

class CustomerSignUpForm(UserCreationForm):
    latitude = forms.FloatField()
    longitude = forms.FloatField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "mobile", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.full_name = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
        if commit:
            user.save()
        return user

class ServiceSignUpForm(UserCreationForm):
    service_name = forms.CharField()
    latitude = forms.FloatField()
    longitude = forms.FloatField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "mobile", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.full_name = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
